from django.conf.urls.defaults import *
from views import index
urlpatterns = patterns('care_apps.dots.views',
    (r'^$', 'index'),
)