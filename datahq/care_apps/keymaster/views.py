from datetime import datetime
import logging
import os
import settings

from django.shortcuts import render_to_response, render_to_string
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponse,Http404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db.models import Q

import uuid

from django_digest.decorators import *
from keymaster.models import DeviceKey
import kzmanage

def get_device_key(request):
    logging.debug(request.GET.keys())
    device_id = request.GET['x-openrosa-deviceid']
    logging.debug(device_id)
    try:
        dev = DeviceKey.objects.all().get(device_id=device_id)
        keyjson = dev.keystring
    except:    
        keyjson = kzmanage.make_device_key(device_id)
        newdev = DeviceKey()
        newdev.device_id = device_id
        newdev.keystring = keyjson
        newdev.key_index = 1
        newdev.location = os.path.join(settings.KEYSTORE_PATH, device_id)
        newdev.save()    
        
    response = HttpResponse(mimetype='text/plain')
    response.write(keyjson) 
    return response        
    