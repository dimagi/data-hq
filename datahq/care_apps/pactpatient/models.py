from django.db import models
from django.utils.translation import ugettext_lazy as _
import uuid
from django.contrib.auth.models import User
from datetime import datetime, timedelta


def make_time():
    return datetime.utcnow()

def make_uuid():
    return uuid.uuid1().hex

# Create your models here.


class IdentifierType(models.Model):
    """
    Placeholder for differing identifiers that may be attached to a patient
    """    
    id = models.CharField(_('Identifier Type Unique id'), max_length=32, unique=True, default=make_uuid, primary_key=True, editable=False)
    description = models.CharField(max_length=64)
    shortname = models.CharField(max_length=32)
    
    regex = models.CharField(max_length=128, blank=True, null=True)
    def save(self):
        super(IdentifierType, self).save()

class Address(models.Model):
    id = models.CharField(_('Identifier Instance Unique id'), max_length=32, unique=True, default=make_uuid, primary_key=True, editable=False)
    type = models.CharField(max_length=24, blank=True, null=True)
    street1 = models.CharField(max_length=160, blank=True, null=True)
    street2 = models.CharField(max_length=160, blank=True, null=True)
    city = models.CharField(max_length=128, blank=True, null=True)
    state = models.CharField(max_length=16, blank=True, null=True)
    postal_code = models.CharField(max_length=12, blank=True, null=True)

class PatientIdentifier(models.Model):
    id = models.CharField(_('Identifier Instance Unique id'), max_length=32, unique=True, default=make_uuid, primary_key=True, editable=False)
    id_type = models.ForeignKey("IdentifierType")
    id_value = models.CharField(max_length=128)    
    
    #todo:  put an update procedure that points all the patient instances to the actual root patient
    def save(self):
        super(PatientIdentifier, self).save()


class Patient(models.Model):
    
    GENDER_CHOICES = (
        ('m', 'Male'),
        ('f', 'Female'),
        )
    
    id = models.CharField(_('Unique Patient uuid PK'), max_length=32, unique=True, default=make_uuid, primary_key=True, editable=False)
    user = models.ForeignKey(User, related_name='patient_user', null=True, unique=True, blank=True)
    
    identifiers = models.ManyToManyField(PatientIdentifier)
    address = models.ManyToManyField(Address)    
    
    dob = models.DateField(_("Date of birth"), null=True, blank=True)
    sex = models.CharField(_("Sex"), choices=GENDER_CHOICES, max_length=1)
    
    is_primary = models.BooleanField(_("Is this patient the primary, merged"), default=True)
    root_patient = models.ForeignKey("self", null=True, blank=True)
    
    added_date = models.DateTimeField(default=make_time)
    
    notes = models.TextField()
      
    @property
    def age(self):
        if not hasattr(self, '_age'):
            td = datetime.utcnow().date() - self.dob
            self._age = int(td.days/365.25)
        return self._age
        
        
    
    def __unicode__(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)
    
    def save(self):
        super(Patient, self).save()
    
    def get_root_patient(self):
        if self.is_primary:
            return self
        else:
            if self.root_patient == None:
                raise Exception ("Error, this patient is designated as not a primary, but the root pointer is null")
            return self.root_patient
        
    def get_all_equivalents(self):
        return Patient.objects.filter(root_patient=self)
    
