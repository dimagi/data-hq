#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

from datetime import datetime, timedelta
from django import forms
from django.contrib.auth.models import User
from django.forms.util import ErrorList, ValidationError
from datetime import datetime
from django.forms import widgets
import hashlib

from provider.models import Provider

class NewProviderForm(forms.ModelForm):    
    username = forms.CharField(max_length=64, required=True)
    first_name = forms.CharField(max_length=64, required=True)
    last_name = forms.CharField(max_length=64, required=True)
    
    email = forms.EmailField(max_length=64, required=True)
    
    password = forms.CharField(max_length=64, widget=forms.PasswordInput())
    password_repeat = forms.CharField(max_length=64, widget=forms.PasswordInput())
    
    
    def clean_username(self):
        data = self.cleaned_data['username']
        if User.objects.filter(username=data).count() > 0:
            raise ValidationError("The username is already taken")
        return data
    
    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).count() > 0:
            raise ValidationError("The email address is already taken")
        return data
    
#    def clean_password(self):
#        if self.cleaned_data['password'] == '':
#            raise ValidationError("Password can't be be blank")
#        return self.cleaned_data['password']
#
#
#    def clean_password_repeat(self):
#        if self.cleaned_data['password_repeat'] == '':
#            raise ValidationError("Password can't be be blank")
#        return self.cleaned_data['password_repeat']

    
    def _do_check_password(self, pone, ptwo):
        if pone == ptwo:
            return pone
        else:
            raise ValidationError("The passwords don't match")
        

    def clean(self):
        """
        Do a default clean and validation, but then set other properties on the case instance before it's saved.
        """
        super(NewProviderForm, self).clean()
        if not self.cleaned_data.has_key('password') and not self.cleaned_data.has_key('password_repeat'):
            raise ValidationError("Password cannot be blank")
        pone = self.cleaned_data['password']
        ptwo = self.cleaned_data['password_repeat']
        self._do_check_password(pone, ptwo)
              
        return self.cleaned_data
    
    def get_user(self):
        try:        
            newuser = User()
            newuser.username = self.cleaned_data['username'] 
            newuser.email = self.cleaned_data['email']
            
            
            newuser.first_name = self.cleaned_data['first_name']            
            newuser.last_name = self.cleaned_data['last_name']
            newuser.is_active = True
            
            password = self.cleaned_data['password']
#            salt = 'j0vviOv'
#            hashed_pass = hashlib.sha1(salt+password).hexdigest()
#            newuser.password = 'sha1$%s$%s' % (salt, hashed_pass)
            newuser.set_password(password)
            newuser.save()
        except Exception, e:
            raise ValidationError("Unable to save user: %s" % e.message)
        return newuser
        
    class Meta:
        model = Provider
        #default exclude for basic editing
        exclude = ('id','user')
