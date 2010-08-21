from django.contrib import admin
from models import *

class ObservationAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(Observation, ObservationAdmin)