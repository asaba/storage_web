from django.shortcuts import render

# Create your views here.


from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.template import loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.context_processors import csrf
from django.db.models import Q
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from models import Tdays, AuthUserGroups, BackendUsed
from django.contrib.auth.decorators import login_required
from django_tables2 import RequestConfig
from tables import TdaysTable_short
from modelforms import SelectBEForm, VerifyHuman
from StringIO import StringIO
import zipfile
import os
from os.path import basename

MAX_FILE_SIZE_BEFORE_DOWNLOAD_BYTES = 4000000000 * 3  # (4GB*3)
fits_extentions = [".fits", ".rf", ".sf", ".cf"]


def index(request):
    logout(request)
    return render_to_response('index.html', {}, context_instance=RequestContext(request))


def builddirectoryfileslist(rootpath):
    result = []
    for root, dirs, files in os.walk(rootpath):
        for name in files:
            result.append(os.path.join(root, name))
    return result


def fitslink_list(request, fits_file_id_list):
    if request.user.username.upper() == "PUBLIC":
        fitslinkpublic(request, fits_file_id_list[0])
    else:
        file_directory_list = []
        file_single_list = []
        for fits_file_id in fits_file_id_list:
            day_record = Tdays.objects.get(pk=fits_file_id)
            tail_path = day_record.filename
            if tail_path[-len(fits_extentions[0])] == fits_extentions[0]:
                #fits file
                #add directory to the list of paths
                file_directory_list.append(os.path.dirname(tail_path))
            else:
                for e in fits_extentions[1:]:
                    if tail_path[-len(e)] == e:
                        # add file to the list of files
                        file_single_list.append(tail_path)

        totalsize = 0
        # calculate total size of directory selected
        for file_directory in file_directory_list:
            for filename in builddirectoryfileslist(file_directory):
                totalsize += os.path.getsize(filename)
        for fsl in file_single_list:
            totalsize += os.path.getsize(fsl)

        if totalsize > MAX_FILE_SIZE_BEFORE_DOWNLOAD_BYTES and len(fits_file_id_list) > 1:
            return listing(request, message="Too many observations selected. (Max 12GB before compression)")
        stream = StringIO()
        temp_zip_file = zipfile.ZipFile(stream, 'w')
        for file_directory in file_directory_list:
            for filename in builddirectoryfileslist(file_directory):
                temp_zip_file.write(filename)
        for fsl in file_single_list:
            temp_zip_file.write(fsl)

        try:
            zipfilename = request.user.username.upper()  # file_directory_list[0].split("/")[-1]
        except:
            zipfilename = "SRTData"

        temp_zip_file.close()
        response = HttpResponse(stream.getvalue(), mimetype='application/zip')
        response['Content-Disposition'] = 'attachment; filename="' + zipfilename + '.zip"'
        return response


def fitslink(request, fits_file_id):
    if request.user.username.upper() == "PUBLIC":
        fitslinkpublic(request, fits_file_id)
    else:
        day_record = Tdays.objects.get(pk=fits_file_id)
        tail_path = day_record.filename
        file_directory = os.path.dirname(tail_path)
        # filename_only = tail_path.split("/")[-1]
        # return HttpResponseRedirect("http://srtmain.oa-cagliari.inaf.it/static" + tail_path)

        stream = StringIO()
        temp_zip_file = zipfile.ZipFile(stream, 'w')

        for filename in builddirectoryfileslist(file_directory):
            temp_zip_file.write(filename, arcname=basename(filename))

        try:
            zipfilename = file_directory.split("/")[-1]
        except:
            zipfilename = "SRTData"

        temp_zip_file.close()
        response = HttpResponse(stream.getvalue(), mimetype='application/zip')
        response['Content-Disposition'] = 'attachment; filename="' + zipfilename + '.zip"'
        return response


def fitslinkpublic(request, fits_file_id):
    verify_form = VerifyHuman()
    request.session["fits_id"] = fits_file_id
    t = loader.get_template("verifyhuman.html")
    c = RequestContext(request, {"verify_form": verify_form, })

    c.update(csrf(request))
    return HttpResponse(t.render(c))


def verify_human(request):
    if request.method == 'POST':
        form = VerifyHuman(request.POST)
        if form.is_valid():
            # you should be able to extract inputs from the form here
            fits_file_id = request.session["fits_id"]
            if fits_file_id is None:
                index(request)
            day_record = Tdays.objects.get(pk=fits_file_id)
            tail_path = day_record.filename
            file_directory = os.path.dirname(tail_path)
            # filename_only = tail_path.split("/")[-1]
            # return HttpResponseRedirect("http://srtmain.oa-cagliari.inaf.it/static" + tail_path)

            stream = StringIO()
            temp_zip_file = zipfile.ZipFile(stream, 'w')

            for filename in builddirectoryfileslist(file_directory):
                temp_zip_file.write(filename, arcname=basename(filename))

            try:
                zipfilename = file_directory.split("/")[-1]
            except:
                zipfilename = "SRTData"

            temp_zip_file.close()
            response = HttpResponse(stream.getvalue(), mimetype='application/zip')
            response['Content-Disposition'] = 'attachment; filename="' + zipfilename + '.zip"'
            request.session["fits_id"] = None
            return response
        else:
            verify_form = VerifyHuman()
            t = loader.get_template("verifyhuman.html")
            c = RequestContext(request, {"verify_form": verify_form, })

            c.update(csrf(request))
            return HttpResponse(t.render(c))
    else:
        verify_form = VerifyHuman()
        t = loader.get_template("verifyhuman.html")
        c = RequestContext(request, {"verify_form": verify_form, })

        c.update(csrf(request))
        return HttpResponse(t.render(c))


def login_user(request):
    state = "Please log in below..."
    username = password = ''
    if request.POST:
        if not request.user.is_authenticated():
            username = request.POST.get('username')
            password = request.POST.get('password')
            if username.upper() == "PUBLIC":
                state = "For public access go to the correct page"
                return render_to_response('auth.html', {'state': state, 'username': username, "request": request, },
                                          context_instance=RequestContext(request))
            else:
                user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # return listing(request)
                    return choisebe(request)
                else:
                    state = "Your account is not active, please contact the site admin."
            else:
                state = "Your username and/or password were incorrect."
        else:
            user = request.user

    elif request.GET:
        return listing(request)

    return render_to_response('auth.html', {'state': state, 'username': username, "request": request, },
                              context_instance=RequestContext(request))


def login_public_user(request):
    state = "Please log in below..."
    username = password = ''
    if request.POST:
        if not request.user.is_authenticated():
            username = request.POST.get('username')
            password = request.POST.get('password')
            if username.upper() != "PUBLIC":
                state = "For PI go to the correct page"
                return render_to_response('auth.html', {'state': state, 'username': username, "request": request, },
                                          context_instance=RequestContext(request))
            else:
                user = authenticate(username=username, password=password)
        else:
            user = request.user
        if user is not None:
            if user.is_active:
                login(request, user)
                # return listing(request)
                return choisebe(request)
            else:
                state = "Your account is not active, please contact the site admin."
        else:
            state = "Your username and/or password were incorrect."
    elif request.GET:
        return listing(request)

    return render_to_response('auth.html', {'state': state, 'username': username, "request": request, },
                              context_instance=RequestContext(request))


# @login_required(login_url='/login/')
def choisebe(request):
    if "backend" in request.session:
        del request.session["backend"]
    choise_be_form = SelectBEForm(initial={'pagination_number': 25,
                                           'backends': backendused(request.user)})
    return render(request, 'select_BE.html', {'choise_be_form': choise_be_form})


# @login_required(login_url='/login/')
def multipledownload(request):
    if request.method == "POST":
        pks = request.POST.getlist("selection")
        return fitslink_list(request, pks)
    elif request.method == "GET":
        pks = request.GET.getlist("selection")
        return fitslink_list(request, pks)


# @login_required(login_url='/login/')
def listing(request, message=None):
    if "backend" in request.session:
        backend_selected = request.session["backend"]
        pagination_number = request.session["pagination_number"]
        source_name = request.session["source_name"]
        frequency_min = request.session["frequency_min"]
        frequency_max = request.session["frequency_max"]
        pointing_position_ra = request.session["pointing_position_ra"]
        pointing_position_dec = request.session["pointing_position_dec"]
        pointing_position_radius = request.session["pointing_position_radius"]
    else:
        if request.method == 'POST':
            form = SelectBEForm(request.POST, initial={'backends': backendused(request.user)})
        else:
            form = SelectBEForm(request.GET, initial={'backends': backendused(request.user)})

        if form.is_valid():
            # you should be able to extract inputs from the form here
            backend_selected = form.cleaned_data["codBE"]
            pagination_number = form.cleaned_data["pagination_number"]
            source_name = form.cleaned_data["source_name"]
            pointing_position_ra = form.cleaned_data["pointing_position_ra"]
            pointing_position_dec = form.cleaned_data["pointing_position_dec"]
            pointing_position_radius = form.cleaned_data["pointing_position_radius"]
            try:
                frequency_min = eval(form.cleaned_data["frequency_min"])
            except:
                frequency_min = 0
            try:
                frequency_max = eval(form.cleaned_data["frequency_max"])
            except:
                frequency_max = 0
            try:
                pointing_position_ra = eval(form.cleaned_data["pointing_position_ra"])
            except:
                pointing_position_ra = None
            try:
                pointing_position_dec = eval(form.cleaned_data["pointing_position_dec"])
            except:
                pointing_position_dec = None
            try:
                pointing_position_radius = eval(form.cleaned_data["pointing_position_radius"])
            except:
                pointing_position_radius = None
            request.session["backend"] = backend_selected
            request.session["pagination_number"] = pagination_number
            request.session["source_name"] = source_name
            request.session["frequency_min"] = frequency_min
            request.session["frequency_max"] = frequency_max
            request.session["pointing_position_ra"] = pointing_position_ra
            request.session["pointing_position_dec"] = pointing_position_dec
            request.session["pointing_position_radius"] = pointing_position_radius
        else:
            backends = []
            ChoiseBEForm = SelectBEForm(initial={"backends": backendused(request.user)})
            return render(request, 'select_BE.html', {'ChoiseBEForm': ChoiseBEForm})

    user = request.user
    dict_x = {}
    if user.id:
        user_group = AuthUserGroups.objects.filter(user=user)
        if len(user_group) > 0:
            groupfilter = Q(project_name="")
            for gf in user_group:
                groupfilter = groupfilter | Q(project_name__iexact=gf.group.name)
            groupfilter = groupfilter & Q(backend__iexact=backend_selected)
            if len(source_name) > 0:
                groupfilter = groupfilter & Q(source__iregex=source_name)
            if frequency_min >= 0 and frequency_max > 0 <= frequency_max:
                groupfilter = groupfilter & Q(frequency__range=(frequency_min, frequency_max))
            if (pointing_position_ra is not None) and (pointing_position_dec is not None) and (
                        pointing_position_radius is not None):
                # calculate range position
                min_pointing_position_ra = pointing_position_ra - pointing_position_radius
                max_pointing_position_ra = pointing_position_ra + pointing_position_radius
                min_pointing_position_dec = pointing_position_dec - pointing_position_radius
                max_pointing_position_dec = pointing_position_dec + pointing_position_radius
                groupfilter = groupfilter & Q(source_ra__range=(min_pointing_position_ra, max_pointing_position_ra))
                groupfilter = groupfilter & Q(source_dec__range=(min_pointing_position_dec, max_pointing_position_dec))

            wanted_items = set()
            paths = {}
            tmp_dir = ""
            for item in Tdays.objects.filter(groupfilter):
                if item.filename.split(".")[-1] == "fits":
                    # if file is a fits file groups in directory
                    tmp_dir = os.path.dirname(item.filename)
                    if tmp_dir in paths:
                        pass
                    else:
                        paths[tmp_dir] = True
                        wanted_items.add(item.pk)
                else:
                    # for file not fits take the single file only
                    wanted_items.add(item.pk)

            tdays_list = Tdays.objects.filter(pk__in=wanted_items)

            # for item in Tdays.objects.filter(groupfilter):
            #     tmp_dir = os.path.dirname(item.filename)
            #     if tmp_dir in paths:
            #         pass
            #     else:
            #         paths[tmp_dir] = True
            #         wanted_items.add(item.pk)
            #
            # tdays_list = Tdays.objects.filter(pk__in=wanted_items)

            if not request.method == 'POST':
                if 'search-persons-post' in request.session:
                    request.POST = request.session['search-persons-post']
                    request.method = 'POST'
            if request.method == 'POST':
                request.session['search-persons-post'] = request.POST
            else:
                pass
            table = TdaysTable_short(tdays_list)
            RequestConfig(request, paginate={"per_page": pagination_number}).configure(table)
            dict_x = {'table': table, "request": request, "message": message, }

            return render_to_response('list.html', dict_x, context_instance=RequestContext(request))

    return render_to_response('list.html', dict_x, context_instance=RequestContext(request))


def backendused(user):
    backends = []
    for g in AuthUserGroups.objects.all().filter(user=user):
        for p in BackendUsed.objects.all().filter(project_name=g.group.name):
            if p.backend not in backends:
                backends.append(p.backend)
    return backends
