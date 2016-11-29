from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from dajaxice.core import dajaxice_autodiscover, dajaxice_config

dajaxice_autodiscover()
admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'srtstorage.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^$', 'storage.views.index'),
                       url(r'^login/$', 'storage.views.login_user'),
                       url(r'^loginpublic/$', 'storage.views.login_public_user'),
                       url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
                       url(r'^choisebe/$', 'storage.views.choisebe'),
                       url(r'^multipledownload/$', 'storage.views.multipledownload'),
                       url(r'^verify/$', 'storage.views.verify_human'),
                       # url(r'^download/$', 'storage.views.download'),
                       url(r'^list/$', 'storage.views.listing'),
                       url(r'^fitslink/(\d+)/$', "storage.views.fitslink", name="fits_link"),
                       url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
                       )

urlpatterns += staticfiles_urlpatterns()
