from django.db import models

from django.utils.translation import ugettext_lazy as _
import uuid
from django.contrib.auth.models import User

def make_uuid():
    return uuid.uuid1().hex



class Provider(models.Model):
    """
    In this current iteration, the provider is *really* dumb and simple.
    """
    
    id = models.CharField(_('Provider Unique id'), max_length=32, unique=True, default=make_uuid, primary_key=True, editable=False)
    user = models.ForeignKey(User, related_name='provider_user') #note, you can be multiple providers for a given user.

    #lame example fields
    job_title = models.CharField(max_length=64)
    affiliation = models.CharField(max_length=64) #am guessing that a providers' affiliations should be FK'ed if they need to be diversified.
    
    def __unicode__(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)
    
    
    def save(self):
        super(Provider, self).save()
