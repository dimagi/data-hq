from django.db import models
from django.contrib.auth.models import User


class DeviceKey(models.Model):
    #user = models.ForeignKey(User)
    device_id = models.CharField(max_length=32)    
    keystring = models.TextField()    
    location = models.TextField()
    key_index = models.PositiveIntegerField(default=1)
    
    