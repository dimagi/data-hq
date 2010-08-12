from django.conf.urls.defaults import *

urlpatterns = patterns('',                      
url(r'^provider/caselist$', 'provider.views.case_list', name='mobile_case_list'),
url(r'^provider/new', 'provider.views.new_provider', name='new_provider'),
)