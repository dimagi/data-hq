import logging
import os
import settings

from corehq.lib.django_digest.decorators import *
from keymaster.models import DeviceKey
import kzmanage

@httpdigest
def get_device_key(request):
    try:
	rosaheader = "HTTP_X_OPENROSA_DEVICEID"
	#'x-openrosa-deviceid'
        device_id = request.META[rosaheader]
    except:
        logging.error("Error, invalid request, no openrosa-deviceid in header")
        response = HttpResponse(mimetype='text/plain')
        response.write("No key") 
        return response
        
    logging.debug(device_id)
    try:
        dev = DeviceKey.objects.all().get(device_id=device_id)
        keyjson = dev.keystring
        #nprint "got it from database"
    except:    
        #nprint "didn't get it from database, trying from file"
        keyjson = kzmanage.make_device_key(device_id)
        #nprint "made it from kzmanage"
        newdev = DeviceKey()
        newdev.device_id = device_id
        newdev.keystring = keyjson
        newdev.key_index = 1
        newdev.location = os.path.join(settings.KEYSTORE_PATH, device_id)
        newdev.save()    
        
    response = HttpResponse(mimetype='text/plain')
    response.write(keyjson) 
    return response        
    
