from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
    url(r'^downloads/$', 'downloads.views.downloads_dashboard', name='downloads'),
    url(r'^downloads/(?P<domain>.*)/$', 'downloads.views.downloads_dashboard_for_domain'),
)
