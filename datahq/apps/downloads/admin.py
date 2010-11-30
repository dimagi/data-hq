from django.contrib import admin
from datahq.apps.downloads.models import *

admin.site.register(JadDownloadItem)
admin.site.register(JarDownloadItem)