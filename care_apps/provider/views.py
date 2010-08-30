from datetime import datetime
import logging

from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponse,Http404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db.models import Q

import uuid

from corehq.lib.django_digest.decorators import *

from provider.forms import  NewProviderForm
from provider.models import Provider
from corehq.apps.domain.models import Domain
from pactpatient.models import Patient, PatientIdentifier, Address, IdentifierType



def get_ghetto_registration_block(user):
    registration_block = """
    <registration>
                <username>%s</username>
                <password>%s</password>
                <uuid>%s</uuid>
                <date>%s</date>
                <registering_phone_id>%s</registering_phone_id>
                <user_data>
                    <data key="promoter_id">%s</data>
                    <data key="promoter_name">%s</data>
                    <data key="promoter_member_id">%s</data>
                </user_data>
                
           </registration>
           """
    #promoter_member_id is the nasty id from the csv, this should be fixed to match the Partners id -->
    resp_txt = ""    
    prov = Provider.objects.filter(user=user)[0] #hacky nasty
    return registration_block % (user.username, user.password, prov.id, user.date_joined.strftime("%Y-%m-%dT%H:%M:%S.000"), uuid.uuid1().hex, user.id, user.first_name, "blah")
    
#    <phone1>asfddsf</phone1> (2 and 3)
#   <address1>concated</address1> (and 2)
    
def get_ghetto_phone_block(patient):
    pnums = patient.identifiers.all().filter(id_type__description='Phone Number')
    ret = ''
    count = 1
    for num in pnums:
        ret += "<phone%d>%s</phone%d>" % (count, num.id_value.replace("(","").replace(")",""), count)
        #ret += "<homephone>%s</homephone>" % (num.id_value)
        count += 1    
    return ret

def get_ghetto_address_block(patient):
    addrs= patient.address.all()
    ret = ''
    count = 1
    for addr in addrs:       
        addconcat = "%s %s, %s %s" % (addr.street1, addr.city, addr.state, addr.postal_code)        
        ret += "<address%d>%s</address%d>" % (count,addconcat, count)
        #ret += "<homeaddress>%s</homeaddress>" % (addconcat)
        count += 1
    
    return ret
    
def get_ghetto_patient_block(patient):
    #2010-05-07T15:52:18.356
    #%Y-%m-%dT%H:%M:%S.000
    patient_block = """<case>
                   <case_id>%s</case_id>
                   <date_modified>%s</date_modified>
                   <create>
                       <case_type_id>cc_path_client</case_type_id>
                       <user_id>%s</user_id>
                       <case_name>%s</case_name>
                       <external_id>%s</external_id>
                   </create>
                   <update>
                       <pactid>%s</pactid>
                       <gender>%s</gender>
                       <type>dot</type>                       
                       %s
                       %s       
                       
                       <dob>%s</dob>                       
                       <initials>%s</initials>
                       <promoters>%s</promoters>
                   </update>
           </case>"""
           
    pactidtype = IdentifierType.objects.get(shortname='PACTID')
    pactid = patient.identifiers.filter(id_type=pactidtype)[0]
    phone_block = get_ghetto_phone_block(patient)
    address_block = get_ghetto_address_block(patient)
    
    promoters_arr = eval(patient.notes)[0].split(':')
    
    
    
    return patient_block %(patient.id, \
                           patient.added_date.strftime("%Y-%m-%dT%H:%M:%S.000"), \
                           patient.user.id, \
                           patient.user.username, \
                           pactid.id_value, \
                           pactid.id_value, \
                           patient.sex,                           
                           phone_block,\
                           address_block,\
                           #patient.dob,
                           '1977-1-1',
 
                           patient.user.first_name[0].lower() + patient.user.last_name[0].lower(),\
                           ' '.join(promoters_arr))
           
@httpdigest
def case_list(request):
    uname = request.user.username
    pwd = request.user.password
    prov_uuid = Provider.objects.get(user=request.user).id
    reg_date = request.user.date_joined
    reg_phone = uuid.uuid1().hex
    chw_guid = uuid.uuid1().hex
    user_id = request.user.id
    first_name = request.user.first_name
    
    #resp_txt = less_static_response % (uname, pwd, prov_uuid, reg_date, reg_phone, user_id, first_name)
    
    
    regblock= get_ghetto_registration_block(request.user)
    patient_block = ""
    for pt in Patient.objects.all():
        patient_block += get_ghetto_patient_block(pt)
    resp_text = "<restoredata>%s %s</restoredata>" % (regblock, patient_block)
    logging.error(resp_text)
    
    response = HttpResponse(mimetype='text/xml')
    response.write(resp_text)
    return response
    
@login_required    
def new_provider(request, template_name="provider/edit_provider.html"):    
    context = {}    
    context['form'] = NewProviderForm()
    if request.method == 'POST':
        form = NewProviderForm(data=request.POST)
        if form.is_valid():
            prov = form.save(commit=False)    
            puser = form.get_user()
            #ugly pact hack
            pact_domain = Domain.objects.get(name='pact')
            membership = pact_domain.add(puser)
            prov.user = puser
            prov.save()
            
            return HttpResponseRedirect('/')
        else:
            context['form'] = form
            
    return render_to_response(template_name, context, context_instance=RequestContext(request))
    
    
    
