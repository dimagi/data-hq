from django.contrib import admin

from django.contrib.auth.models import User
from models import *




class ProviderAdmin(admin.ModelAdmin):
    list_display=('id', 'user', 'job_title', 'affiliation', )
    list_filter = ['job_title','affiliation']
    
admin.site.register(Provider, ProviderAdmin)