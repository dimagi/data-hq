import os
from django.conf import settings
from domain.decorators import login_and_domain_required
from webutils import render_to_response
from django.http import HttpResponse, HttpResponseServerError, HttpResponseBadRequest, HttpResponseNotFound
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from datahq.apps.downloads.models import JJUploadForm, JarDownloadItem
from datahq.apps.downloads.models import JadDownloadItem, JadDownloadItem
from datahq.apps.downloads import utils
from django.core.servers.basehttp import FileWrapper

JAVAROSA_LINK = settings.DATAHQ_URL+"/download/"
JAVAROSA_VERSION="1.0"

def downloads_dashboard(request, template_name="downloads/downloads.html"):
    context = {}
    links = {}
    
    user = request.user
    if not (user.is_authenticated() and user.is_active):
        context.update({"message":"To get a customized version of JavaRosa for your domain, please login."})
    else: #user is indeed logged in
        if user.selected_domain is not None:
            return HttpResponseRedirect(str(user.selected_domain))           
        else:
            context.update({"message": "User has not selected a domain! To download a customized version of Javarosa please select a HQ Domain."})
    
    links.update({"J2ME Javarosa Standard with Default Settings": {"version":JAVAROSA_VERSION,"link":JAVAROSA_LINK}})
             
    context["links"]=links
    context['upload_form'] = JJUploadForm()
    context['show_upload'] = False
    

    return render_to_response(request, template_name, context)

@login_and_domain_required
def downloads_dashboard_for_domain(request, domain, template_name="downloads/downloads.html"):
    if domain is None:
        return downloads_dashboard(request)
    
    if request.method == 'POST':
        return app_upload(request, domain)
    context = {}
    context.update({"domain":str(domain)})
    links = {}
    href = JAVAROSA_LINK+str(domain)
    links.update({"J2ME Javarosa Standard with Default Settings": {"version":JAVAROSA_VERSION,"link":JAVAROSA_LINK}})
    links.update({"<b>Custom Javarosa version for domain: "+str(domain).upper()+"</b>": {"version":JAVAROSA_VERSION,"link":href}})    
             
    context["links"]=links
    context['upload_form'] = JJUploadForm()
    context['show_upload'] = True
    return render_to_response(request, template_name, context)

def app_upload(request, domain):
    form = JJUploadForm(request.POST, request.FILES) # A form bound to the POST data
    if form.is_valid(): # All validation rules pass
        #save the files to disk
        jar_f = request.FILES['jar']
        jar_name = form.cleaned_data['name'] + '_jar'
        jad_f = request.FILES['jad']
        jad_name = form.cleaned_data['name'] + '_jad'
        
        jar_path, jad_path = save_jar_jad_to_disk(jar_f,jar_name,jad_f,jad_name)
        
        # Create the Jar+Jad model items
        jar = JarDownloadItem(uri=jar_path,name=form.cleaned_data['name'])
        jar.description = form.cleaned_data['description']
        jar.version = form.cleaned_data['version']
        jar.domain = request.user.selected_domain
        jar.save()
        
        jad = JadDownloadItem(uri=jad_path,jar=jar,is_original=True)
        jad.version = form.cleaned_data['version']
        jad.description = form.cleaned_data['description']
        jad.jar = jar
        jad.save()
        
        return HttpResponse('Woot! It worked!') # Redirect after POST
    else:
        return HttpResponse("Form invalid.")
    
    
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

@login_and_domain_required
def thanks(request):
    HttpResponse("Cool, seems to have worked.")
    
    
#def download_default_jad(request):
#    jad = utils.find_or_create_default_jad()
#    
#    if jad:
#        try:
#            response = HttpResponse(mimetype='text/vnd.sun.j2me.app-descriptor')
#            response.write(utils.get_contents(jad))
#            return response
#        except:
#            return ""
#    else: #this should never happen
#        return HttpResponseNotFound()
#    
#
#def download_default_jar(request):
#    jar = utils.find_or_create_default_jar()
#    
#    if jar:
#        try:
#            response = HttpResponse(mimetype='application/java-archive')
#            response.write(utils.get_contents(jar))
#            return response
#        except:
#            return ""
#    else: #this should never happen
#        return HttpResponseNotFound()
    
def download_jad(request, domain=None):
    jad = utils.find_or_create_domain_jad(domain)
    
    if jad:
        try:
            response = HttpResponse(mimetype='text/vnd.sun.j2me.app-descriptor')
            response.write(utils.get_contents(jad))
            response["content-disposition"] = 'attachment; filename="%s"' % os.path.basename(jad.uri)
            return response
        except:
            return ""
    else: #this should never happen
        return HttpResponseNotFound()
    
def download_default_jad(request):
    return download_jad(request,domain=None)


def download_default_jar(request):
    return download_jar(request,domain=None)
    
def download_jar(request, domain=None):
    if not domain:
        jar = utils.find_or_create_domain_jar(None)
    else:
        jar = utils.find_or_create_domain_jar(domain)
    
    if jar:
        try:
            d=""
            if domain: d=domain
            else: d="default"
            static_path = settings.MEDIA_URL+"/downloads/apps/"+d+"/"+os.path.basename(jar.uri)
            return HttpResponseRedirect(static_path)
#            f = open(jar.uri.replace("/","\\"),'r').read()
##            wrapper = open(f,'r')
#            response = HttpResponse(f, mimetype='application/java-archive')
##            response.write(utils.get_contents(jar))
#            response['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(jar.uri)
#            print 'PATH IS ' + str(jar.uri)
#            response['Content-Length'] = os.path.getsize(jar.uri)
#            
##            f.seek(0)
#            return response
        except:
            return ""
    else: #this should never happen
        return HttpResponseNotFound()