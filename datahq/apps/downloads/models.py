from django.db import models
from datahq.apps.domain.models import Domain
from django import forms
from datahq.shared_code.multifile import multifile

class JarDownloadItem(models.Model):
    
    
    description = models.CharField(max_length=255)
    uri = models.CharField(max_length=255, blank=False, null=False)  #path to file on disk or web url
    version = models.CharField(max_length=255)
    domain = models.ForeignKey(Domain)
    name = models.CharField(max_length=255, blank=False, null=False)
    
    def __unicode__(self):
        return "Name: "+self.filename + ", Ver: "+self.version+ ", Description: "+self.description


# Create your models here.
'''
Create a JAD class ?  Might be good to create them and link them to a domain and DownloadItem, instead of saving them to the disk as files.
This looks like it would be an ideal use of an existing couchdb.
'''
# Framework:
# Read existing JAD file (associated with DownloadItem maybe? Is that always guaranteed? Should it be?)
# Look for the relevant URL Params that need to be adjusted according to domain (see clayton's email/confluence page)
# Make the changes
# Copy the resulting jad file wholesale into the db (it's usually no more than 15 short lines of text)
# Next time someone goes to the designated url (something like http://datahq.org/<domain>/app/download or whatever) serve
# up the correct Jad.  When they go to get the Jar, that remains the plain vanilla one and everything should just work.  Awesome.

class JadDownloadItem(models.Model):
    uri = models.CharField(max_length=255, blank=False, null=False)
    form_list_url = models.CharField(max_length=255)
    form_post_url = models.CharField(max_length=255)
    version = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    is_original = models.BooleanField(null=False,blank=False,description="Is this the original Jad that came with the Jar?")
    jar = models.ForeignKey(JarDownloadItem, null=False, blank=False)
    
    def __unicode__(self):
        return "Version: "+self.version + ", Description: "+self.description
    
    
class JJUploadForm(forms.Form):
    jar = forms.FileField(max_length=255)
    jad = forms.FileField(max_length=255)
    name = forms.CharField(max_length=255)
    description = forms.Textarea(max_length=255)
    version = forms.CharField(max_length=255)