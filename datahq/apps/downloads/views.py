import os
from django.conf import settings
from domain.decorators import login_and_domain_required
from webutils import render_to_response
from django.http import HttpResponse, HttpResponseServerError, HttpResponseBadRequest, HttpResponseNotFound
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from datahq.apps.downloads.models import JJUploadForm, JarDownloadItem
from datahq.apps.downloads.models import JadDownloadItem, JadDownloadItem

JAVAROSA_FILENAME="somejad.jad"
JAVAROSA_VERSION="1.0"

def downloads_dashboard(request, template_name="downloads/downloads.html"):
    context = {}
    links = {}
    
    user = request.user
    if not (user.is_authenticated() and user.is_active):
        context.update({"message":"To get a customized version of JavaRosa for your domain, please login."})
    else: #user is indeed logged in
        if user.selected_domain is not None:
            context.update({"domain":str(user.selected_domain)})
            href = "downloads/"+str(user.selected_domain)+"/jr/"+JAVAROSA_FILENAME
            links.update({"<b>Custom Javarosa version for domain: "+str(user.selected_domain).upper()+"</b>": {"version":JAVAROSA_VERSION,"link":href}})
        else:
            context.update({"message": "User has not selected a domain! To download a customized version of Javarosa please select a HQ Domain."})
    
    links.update({"J2ME Javarosa Standard with Default Settings": {"version":JAVAROSA_VERSION,"link":"downloads/jr/"+JAVAROSA_FILENAME}})
             
    context.update({"links":links})

    return render_to_response(request, template_name, context)

@login_and_domain_required
def downloads_dashboard_for_domain(request, domain, template_name="downloads/downloads.html"):
    if domain is None:
        return downloads_dashboard(request)
    
    context = {}
    context.update({"domain":str(domain)})
    links = {}
    href = "downloads/"+str(domain)+"/jr/"+JAVAROSA_FILENAME
    links.update({"J2ME Javarosa Standard with Default Settings": {"version":JAVAROSA_VERSION,"link":"downloads/jr/"+JAVAROSA_FILENAME}})
    links.update({"<b>Custom Javarosa version for domain: "+str(domain).upper()+"</b>": {"version":JAVAROSA_VERSION,"link":href}})    
             
    context.update({"links":links})

    return render_to_response(request, template_name, context)

@login_and_domain_required
def app_upload(request):
    if request.method == 'POST': # If the form has been submitted...
        form = JJUploadForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            #save the files to disk
            jar_f = request.FILES['jar']
            jar_name = form.name + '_jar'
            jad_f = request.FILES['jad']
            jad_name = form.name + '_jad'
            
            jar_path, jad_path = save_jar_jad_to_disk(jar_f,jar_name,jad_f,jad_name)
            
            # Create the Jar+Jad model items
            jar = JarDownloadItem(uri=jar_path,name=form.name)
            jar.description = form.description
            jar.version = form.version
            jar.domain = request.user.selected_domain
            jar.save()
            
            jad = JadDownloadItem(uri=jad_path,jar=jar,is_original=True)
            jad.version = form.version
            jad.description = form.description
            jad.save()
            
            return HttpResponseRedirect('/thanks/') # Redirect after POST
    else:
        form = JJUploadForm() # An unbound form

    return render_to_response('contact.html', {
        'form': form,
    })
    
    
    
def save_jar_jad_to_disk(jar,jar_name,jad,jad_name):
    jar_path = save_file_to_disk(settings.UPLOADED_APP_STORAGE_PATH,jar,jar_name)
    jad_path = save_file_to_disk(settings.UPLOADED_APP_STORAGE_PATH,jad,jad_name)
    
    return jar_path, jad_path
    
def save_file_to_disk(path,f,name):
    """
    Saves file to disk and returns its path
    """
    p = os.path.join(path,name)
    destination = open(p, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    
    return p