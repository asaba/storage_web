'''
Created on 13/dic/2015

@author: sabah
'''

import django_tables2 as tables
from django.utils.safestring import mark_safe
from django_tables2 import A

from models import Tdays


class TestTable(tables.Table):
    songid = tables.Column()
    links = tables.LinkColumn("playsongid", kwargs={"songid": A("songid")})


class TdaysTable(tables.Table):
    # download_link = CustomTextLinkColumn('my_app.views.personal_page_view', args=[A('personal_webpage')],
    #     custom_text='Personal Webpage', verbose_name='Personal Webpage', )

    class Meta:
        model = Tdays
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}


class TdaysTable_short(TdaysTable):
    # filename = tables.URLColumn()
    selection = tables.CheckBoxColumn(accessor='pk', orderable=False)

    # download_link = tables.LinkColumn('fits_link', args=[A("pk")], empty_values=(), verbose_name='Download')

    # def render_filename(self, value):
    #    return '<a href="{path}">Download</a>'.format(path = value)

    # def render_download_link(self, record, value, column, bound_column, bound_row):
    #    return mark_safe('<a href="{path}">Download</a>'.format(path = record.pk))

    class Meta:
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        exclude = ("id", "filename", "idtdays", "telescope", "project_dir", "schedulename", "mjd_start", "mjd_stop",)
        sequence = (
        'selection', "date", "source", "project_name", "frequency", "bandwidth", "localoscillator", "samplerate",
        "receiver", "backend", "source_ra", "source_dec")
