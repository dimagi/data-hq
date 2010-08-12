from django.conf.urls.defaults import *

urlpatterns = patterns('',                      
    url(r'^keys/getkey$', 'keymaster.views.get_device_key', name='get_device_key'),
)