from django.conf.urls.defaults import *

urlpatterns = patterns('care_apps.dots.views',
    (r'^$', 'index'),
)