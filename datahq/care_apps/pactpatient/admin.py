from django.contrib import admin
from reversion.admin import VersionAdmin
from django.contrib.auth.models import User
from models import *

class IdentifierTypeAdmin(admin.ModelAdmin):
    list_display=('id', 'description','shortname', 'regex',)
    list_filter = []

admin.site.register(IdentifierType, IdentifierTypeAdmin)

class PatientIdentifierAdmin(VersionAdmin):
    list_display=('id', 'id_type', 'patient', 'id_value',)
    list_filter = ['id_type', 'patient']
admin.site.register(PatientIdentifier, PatientIdentifierAdmin)

class AddressAdmin(VersionAdmin):
    list_display=('type', 'street1', 'street2', 'city', 'state', 'postal_code')
    list_filter = ['type','city','state','postal_code']        
admin.site.register(Address, AddressAdmin)

class PatientIdentifierInline(admin.StackedInline):
    model = PatientIdentifier    

class AddressInline(admin.StackedInline):
    model = Address

class PatientAdmin(admin.ModelAdmin):
    list_display=('id', 'user', 'dob', 'is_primary')
    list_filter = []
    inlines = [PatientIdentifierInline, AddressInline]    
admin.site.register(Patient, PatientAdmin)


