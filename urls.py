# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('fshare.views',

    url(r'^$', 'index_page', name='index'),
    url(r'^success_upload/(?P<fileset>\d+)', 'success_upload', name='success_upload'),
    url(r'^download/(?P<fileset>\d+)', 'download', name='download'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    (r'^%s(?P<path>.*)$' % settings.MEDIA_URL.lstrip('/'),
        'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)

urlpatterns += patterns('',
    (r'^%s(?P<path>.*)$' % settings.STATIC_URL.lstrip('/'),
        'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )