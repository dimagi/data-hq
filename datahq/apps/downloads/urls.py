from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
    url(r'^downloads/$', 'downloads.views.downloads_dashboard', name='downloads'),
    url(r'^downloads/(?P<domain>.*)/$', 'downloads.views.downloads_dashboard_for_domain'),
    url(r'^download/$', 'downloads.views.download_default_jad'),
    url(r'^download/jar/$', 'downloads.views.download_default_jar'),
    url(r'^download/(?P<domain>.*)/jar/$', 'downloads.views.download_jar'),
    url(r'^download/(?P<domain>.*)/$', 'downloads.views.download_jad'),
    url(r'^app/default/download/$', 'downloads.views.download_default_jad'),
    url(r'^app/(?P<domain>.*)/$', 'downloads.views.download_jad'),

)
