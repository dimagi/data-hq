from datetime import datetime
import logging
import os
import settings

from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponse,Http404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.shortcuts import render_to_response


from xforms.models import FormDefModel
from domain.decorators import login_and_domain_required


from pactdata.models import SchemaPactTeNoteProgressNoteNoteReferralsReferral5, SchemaPactPactProgressNote5, SchemaPactEssNoteNoteProgressNoteNoteBwresultsBw5
import uuid

@login_and_domain_required
def patients(request):
    pass

@login_and_domain_required
def progress_notes(request, template_name="pactapp/progress_notes.html"):
    context = RequestContext(request)
    all_notes = SchemaPactPactProgressNote5.objects.all()
    context['notes']  = all_notes    
    return render_to_response(template_name, context_instance=context)
    

@login_and_domain_required
def progress_note(request, submit_id, template_name="pactapp/progress_note.html"):    
    context = RequestContext(request)
    
    xform = FormDefModel.objects.get(id=7) #hacky hack
    # for now, the formdef version/uiversion is equivalent to 
    # the instance version/uiversion
    data = [('XMLNS',xform.target_namespace), ('Version',xform.version), 
            ('uiVersion',xform.uiversion)]
    attach = xform.get_attachment(submit_id)
    row = xform.get_row(submit_id)
    fields = xform.get_display_columns()
    # make them a list of tuples of field, value pairs for easy iteration
    data = data + zip(fields, row)
    
    referrals = SchemaPactTeNoteProgressNoteNoteReferralsReferral5.objects.all().filter(parent_id=submit_id)
    bloodworks = SchemaPactEssNoteNoteProgressNoteNoteBwresultsBw5.objects.all().filter(parent_id=submit_id)
    
    context['referrals'] = referrals
    context['bloodworks'] = bloodworks
    
    context.update({"form" : xform, "id": submit_id, "data": data, "attachment":attach })    
    return render_to_response(template_name, context_instance=context)    
    
    
    
