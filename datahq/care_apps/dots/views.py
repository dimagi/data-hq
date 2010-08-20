from django.shortcuts import render_to_response
#from django.http import HttpResponse
from domain.decorators import login_and_domain_required
from django.template import RequestContext

# Create your views here.
@login_and_domain_required
def index(request, template='dots/index.html'):
    context = RequestContext(request)
    return render_to_response(template, context)