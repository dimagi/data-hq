from django.conf.urls.defaults import *

urlpatterns = patterns('',    
    url(r'^pact/notes/$', 'care_apps.pactapp.views.progress_notes', name='progress_notes'),
    url(r'^pact/note/(?P<submit_id>\d+)/$', 'care_apps.pactapp.views.progress_note', name='progress_note'),
)
