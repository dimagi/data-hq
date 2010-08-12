from django.conf.urls.defaults import *

urlpatterns = patterns('',    
    url(r'^pact/notes/$', 'pactapp.views.progress_notes', name='progress_notes'),
    url(r'^pact/note/(?P<submit_id>\d+)/$', 'pactapp.views.progress_note', name='progress_note'),
)
