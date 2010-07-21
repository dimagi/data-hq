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

from django_digest.decorators import *

from provider.forms import  NewProviderForm
from provider.models import Provider
from domain.models import Domain

less_static_response = """
<restoredata>
           <registration>
                <username>%s</username>
                <password>%s</password>
                <uuid>%s</uuid>
                <date>%s</date>
                <registering_phone_id>%s</registering_phone_id>
                <user_data>
                    <data key="promoter_id">%s</data>
                    <data key="promoter_name">%s</data>
                </user_data>
           </registration>
           <case>
                   <case_id>04CBE782D762341234B2E224577A</case_id>
                   <date_modified>2010-05-07T15:52:18.356</date_modified>
                   <create>
                       <case_type_id>cc_path_client</case_type_id>
                       <user_id>3F2504E04F8911D39A0C0305E82C3301</user_id>
                       <case_name>22</case_name>
                       <external_id>22</external_id>
                   </create>
                   <update>
                       <pactid>22</pactid>
                       <gender>M</gender>
                       <type>dot</type>
                       <homephone>617-555-1111</homephone>
                       <cellphone>617-555-2222</cellphone>
                       <dob>1991-03-22</dob>
                       <homeaddress>234 Fake St. Boston, MA</homeaddress>
                       <initials>ABC</initials>
                   </update>
           </case>
           <case>
                   <case_id>04C2412341F3CB825E4B2E224577A</case_id>
                   <date_modified>2010-06-07T15:52:18.356</date_modified>
                   <create>
                       <case_type_id>cc_path_client</case_type_id>
                       <user_id>3F2504E04F8911D39A0C0305E82C3301</user_id>
                       <case_name>25</case_name>
                       <external_id>25</external_id>
                   </create>
                   <update>
                       <pactid>25</pactid>
                       <gender>F</gender>
                       <type>hiv</type>
                       <homephone>617-555-1112</homephone>
                       <cellphone>617-555-2221</cellphone>
                       <dob>1994-05-12</dob>
                       <homeaddress>432 Unreal Ave. Roxbury, MA</homeaddress>
                       <initials>GEC</initials>
                   </update>
           </case>
           <case>
                   <case_id>04CBE782D763453245324224577A</case_id>
                   <date_modified>2010-07-07T15:52:18.356</date_modified>
                   <create>
                       <case_type_id>cc_path_client</case_type_id>
                       <user_id>3F2504E04F8911D39A0C0305E82C3301</user_id>
                       <case_name>29</case_name>
                       <external_id>29</external_id>
                   </create>
                   <update>
                       <pactid>29</pactid>
                       <gender>M</gender>
                       <type>dot</type>
                       <homephone>505-363-8405</homephone>
                       <cellphone>505-363-8405</cellphone>
                       <dob>1986-03-22</dob>
                       <homeaddress>61 Night St. Somerville, MA</homeaddress>
                       <initials>CTS</initials>
                   </update>
           </case>
           <case>
                   <case_id>2341324D32D634F3CB825E4B2E224577A</case_id>
                   <date_modified>2010-04-07T15:52:18.356</date_modified>
                   <create>
                       <case_type_id>cc_path_client</case_type_id>
                       <user_id>3F2504E04F8911D39A0C0305E82C3301</user_id>
                       <case_name>36</case_name>
                       <external_id>36</external_id>
                   </create>
                   <update>
                       <pactid>36</pactid>
                       <gender>M</gender>
                       <type>dot</type>
                       <cellphone>617-555-6922</cellphone>
                       <dob>1984-02-11</dob>
                       <homeaddress>234 Night St. Roxbury, MA</homeaddress>
                       <initials>IK</initials>
                   </update>
           </case>
           <case>
                   <case_id>SPD9F8JH23H9283HF9328HFR2938F</case_id>
                   <date_modified>2010-03-07T15:52:18.356</date_modified>
                   <create>
                       <case_type_id>cc_path_client</case_type_id>
                       <user_id>3F2504E04F8911D39A0C0305E82C3301</user_id>
                       <case_name>38</case_name>
                       <external_id>38</external_id>
                   </create>
                   <update>
                       <pactid>38</pactid>
                       <gender>M</gender>
                       <type>hiv</type>
                       <homephone>617-555-4724</homephone>
                       <dob>1970-11-02</dob>
                       <homeaddress>4 Circle Dr. Boston, MA</homeaddress>
                       <initials>VME</initials>
                   </update>
           </case>
           <case>
                   <case_id>ASDF09JQ209J0932HJ0F92JF029F</case_id>
                   <date_modified>2010-01-03T15:52:18.356</date_modified>
                   <create>
                       <case_type_id>cc_path_client</case_type_id>
                       <user_id>3F2504E04F8911D39A0C0305E82C3301</user_id>
                       <case_name>45</case_name>
                       <external_id>45</external_id>
                   </create>
                   <update>
                       <pactid>45</pactid>
                       <gender>F</gender>
                       <type>dot</type>
                       <homephone>617-555-3423</homephone>
                       <cellphone>617-555-6264</cellphone>
                       <dob>1955-05-01</dob>
                       <homeaddress>9943 Square Rd. Lynn, MA</homeaddress>
                       <initials>FPA</initials>
                   </update>
           </case>
        </restoredata>"""


static_response = """
<restoredata>
           <registration>
                <username>ctsims</username>
                <password>234</password>
                <uuid>3F2504E04F8911D39A0C0305E82C3301</uuid>
                <date>2009-08-12</date>
                <registering_phone_id>3F2504E04F8911D39A0C0305E82C3301</registering_phone_id>
                <user_data>
                    <data key="promoter_id">33</data>
                    <data key="promoter_name">Clayton</data>
                </user_data>
           </registration>
           <case>
                   <case_id>04CBE782D762341234B2E224577A</case_id>
                   <date_modified>2010-05-07T15:52:18.356</date_modified>
                   <create>
                       <case_type_id>cc_path_client</case_type_id>
                       <user_id>3F2504E04F8911D39A0C0305E82C3301</user_id>
                       <case_name>621145448</case_name>
                       <external_id>2</external_id>
                   </create>
                   <update>
                       <pact_id>2</pact_id>
                   </update>
           </case>
           <case>
                   <case_id>04C2412341F3CB825E4B2E224577A</case_id>
                   <date_modified>2010-06-07T15:52:18.356</date_modified>
                   <create>
                       <case_type_id>cc_path_client</case_type_id>
                       <user_id>3F2504E04F8911D39A0C0305E82C3301</user_id>
                       <case_name>631145448</case_name>
                       <external_id>3</external_id>
                   </create>
                   <update>
                       <pact_id>3</pact_id>
                   </update>
           </case>
           <case>
                   <case_id>04CBE782D763453245324224577A</case_id>
                   <date_modified>2010-07-07T15:52:18.356</date_modified>
                   <create>
                       <case_type_id>cc_path_client</case_type_id>
                       <user_id>3F2504E04F8911D39A0C0305E82C3301</user_id>
                       <case_name>551145448</case_name>
                       <external_id>5</external_id>
                   </create>
                   <update>
                       <pact_id>5</pact_id>
                   </update>
           </case>
           <case>
                   <case_id>2341324D32D634F3CB825E4B2E224577A</case_id>
                   <date_modified>2010-04-07T15:52:18.356</date_modified>
                   <create>
                       <case_type_id>cc_path_client</case_type_id>
                       <user_id>3F2504E04F8911D39A0C0305E82C3301</user_id>
                       <case_name>661145448</case_name>
                       <external_id>6</external_id>
                   </create>
                   <update>
                       <pact_id>6</pact_id>
                   </update>
           </case>
        </restoredata>
"""

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
    
    resp_txt = less_static_response % (uname, pwd, prov_uuid, reg_date, reg_phone, user_id, first_name)
    response = HttpResponse(mimetype='text/xml')
    response.write(resp_txt)
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
    
    
    
