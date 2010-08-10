from django.db import models
from tracking.models import Visitor
import uuid
from datetime import datetime
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User

def make_uuid():
    return uuid.uuid1().hex
def getdate():
    return datetime.utcnow()

class AuditEvent(models.Model):
    pass

class FieldAccess(models.Model):
    object_type = models.ForeignKey(ContentType, verbose_name='Case linking content type', blank=True, null=True)
    field = models.CharField(max_length=64, blank=True, null=True)
    
    class Meta:
        unique_together = ('object_type', 'field')
    

class ModelAccessLog(models.Model):    
    id = models.CharField(_('Access guid'), max_length=32, unique=True, default=make_uuid, primary_key=True) #primary_key override?
    
    object_type = models.ForeignKey(ContentType, verbose_name='Case linking content type', blank=True, null=True)
    object_uuid = models.CharField('object_uuid', max_length=32, db_index=True, blank=True, null=True)
    content_object = generic.GenericForeignKey('object_type', 'object_uuid')
    
    properties = models.ManyToManyField(FieldAccess, blank=True, null=True)
    property_data = models.TextField() #json of the actual fields accessed
    
    user = models.ForeignKey(User)
    accessed = models.DateTimeField(default = getdate())

#
#class ModelAuditEvent(models.Model):
#    session_key = models.CharField(max_length=40)
#    ip_address = models.CharField(max_length=20)
#    user = models.ForeignKey(User, null=True)
#    user_agent = models.CharField(max_length=255)
#    referrer = models.CharField(max_length=255)
#    url = models.CharField(max_length=255)
#    page_views = models.PositiveIntegerField(default=0)
#    session_start = models.DateTimeField()
#    last_update = models.DateTimeField()