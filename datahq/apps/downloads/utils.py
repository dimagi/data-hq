"""
Create methods for parsing the Jad file and replacing fields.  Make it a generic method, in the sense that
you should be able to specify a variable and it's value.  If it's not there, it should be created, if it is
there it should be modified.
"""

import fileinput
import sys
import os
import shutil
import logging
from datahq.apps.downloads.models import JarDownloadItem, JadDownloadItem
from django.conf import settings
from datahq.apps.domain.models import Domain
import logging

#ROOT = os.path.abspath(.)



def set_midlet_url(jad, new_url):
    '''
    This takes in a jad file path and alters the MIDlet-Jar-URL: param for the actual JAD to the specified url
    '''
    _replaceAll(jad, "MIDlet-Jar-URL:", "MIDlet-Jar-URL: "+new_url+"\r\n")
    
def set_JRDemo_Post_Url(jad, new_url):
    '''
    Sets the JRDemo-Post-Url to specified
    '''
    _replaceAll(jad, "JRDemo-Post-Url:", "JRDemo-Post-Url: "+new_url+"\r\n")

def set_JRDemo_Post_Url_List(jad, new_url):
    '''
    Sets the JRDemo-Post-Url-List to specified
    '''
    _replaceAll(jad, "JRDemo-Post-Url-List:", "JRDemo-Post-Url-List: "+new_url+"\r\n")
    _replaceAll(jad, "Form-Server-Url:", "Form-Server-Url: "+new_url+"\r\n")

#def _replaceAll(file,searchExp,replaceExp):
#    for line in fileinput.input(file, inplace=1):
#        if searchExp in line:
#                line = line.replace(line,replaceExp)
#        
#    return

def _replaceAll(file,searchExp,replaceLine):        
    f = open(file,'r')
    temppath = file+"temp"
    ftemp = open(temppath,'w')
    
    for line in f:
        if searchExp in line:
            line = replaceLine
        ftemp.write(line)
    f.close()
    ftemp.close()
    shutil.move(temppath,file)
        
def findParamInfo(file,searchExp):
    if(searchExp.find(":") == -1):
        searchExp = searchExp.strip() + ": "
    else:
        searchExp = searchExp.strip() + " "
    f = open(file,'r')
    str = None
    for line in f:
        if searchExp in line:
            str = line.split(searchExp).pop()
            break
    f.close()
    return str

    
def edit_jad(jad_file_loc, domain, post_url, list_url):
    midlet_url = settings.DATAHQ_URL+"/download/"+str(domain)+"/jar"
    if domain == "default":
        post_url = settings.JAVAROSA_DEFAULT_POST_URL
        form_list_url = settings.JAVAROSA_DEFAULT_FORM_LIST_URL
    else:
        post_url = post_url
        form_list_url = post_url+"/formList"
        
    set_JRDemo_Post_Url(jad_file_loc, post_url)
    set_JRDemo_Post_Url_List(jad_file_loc, form_list_url)
    set_midlet_url(jad_file_loc, midlet_url)

def find_or_create_domain_jad(domain=None):
    if domain:
        jads = JadDownloadItem.objects.filter(jar__domain__name=domain)
        domain_app_folder = os.path.join(settings.UPLOADED_APP_STORAGE_PATH,str(domain))
    else:
        jads = JadDownloadItem.objects.filter(is_original=True)
        domain_app_folder = os.path.join(settings.UPLOADED_APP_STORAGE_PATH,"default")
        
    default_jr_path = settings.JAVAROSA_DEFAULT_JAR_PATH
    default_jr_path_jad = default_jr_path.replace(".jar",".jad")
    
    jad_file_name = os.path.basename(default_jr_path).replace(".jar",".jad")
    jad_file_loc = os.path.join(domain_app_folder, jad_file_name)
    if domain:
        jar = find_or_create_domain_jar(domain)
    else:
        jar = find_or_create_domain_jar(None)
        domain = "default"
    
    if not os.path.exists(jad_file_loc):
        if os.path.exists(os.path.dirname(jad_file_loc)):
            shutil.copy(default_jr_path_jad, jad_file_loc)
        else: #This folder should always already exist (see call to find_or_create_domain_jar() above)
            raise Exception("Attempted to create Jad with no accompanying Jar in downloads.utils.find_or_create_domain")
    
    if len(jads) == 0:
        uri = jad_file_loc
        
        #create the new model entry
        jad = JadDownloadItem(uri=uri,jar=jar,is_original=False)
        ver = findParamInfo(jad_file_loc,"App-Version")
        if not ver:
            ver = settings.JAVAROSA_DEFAULT_JAR_VERSION
        jad.version = ver
        jad.description = "Auto Genereated Jad for domain "+str(domain)
        midlet_url = settings.DATAHQ_URL+"/download/"+str(domain)+"/jar"
        jad.midlet_url = midlet_url
        
        post_url = settings.DATAHQ_URL+"/receiver/submit/"+str(domain)
        if domain == "default":
            jad.form_post_url = settings.JAVAROSA_DEFAULT_POST_URL
            jad.form_list_url = settings.JAVAROSA_DEFAULT_FORM_LIST_URL
        else:
            jad.form_post_url = post_url
            jad.form_list_url = post_url+"/formList"

        jad.save()
    else:
        jad = jads[0]
        
    edit_jad(jad_file_loc,domain,jad.form_post_url,jad.form_list_url)
    return jad

def find_or_create_domain_jar(domain=None):
    if domain:
        jars = JarDownloadItem.objects.filter(domain__name=domain)
    else:
        jars = JarDownloadItem.objects.filter(default_version=True)
        domain = "default"
        
    
    if len(jars) == 0:
        default_jr_path = settings.JAVAROSA_DEFAULT_JAR_PATH

        if not os.path.exists(default_jr_path):
            raise Exception("JAVAROSA DEFAULT JAR NOT FOUND! path="+settings.JAVAROSA_DEFAULT_JAR_PATH+",,,,,,,"+str(os.getcwd()))
            return False
        
        
        domain_app_folder = os.path.join(settings.UPLOADED_APP_STORAGE_PATH,str(domain))
        domain_app_jar_path = os.path.join(domain_app_folder,os.path.basename(default_jr_path))
        domain_app_jad_path = domain_app_jar_path.replace(".jar",".jad")
        
        default_jad_path = default_jr_path.replace(".jar",".jad")
        
        #if jar for this domain doesn't exist
        #copy the default jar into apps/<domain_name> and use that.
        if os.path.exists(domain_app_folder):
            shutil.copy(default_jr_path,domain_app_folder)
            shutil.copy(default_jad_path,domain_app_folder) #don't forget to copy the jad over too
            uri = domain_app_jar_path
        else:
#            print "TRYING TO MAKE PATH HERE!  "+str(os.path.abspath(domain_app_folder))
#            logging.error("TRYING TO MAKE PATH HERE!  "+str(os.path.abspath(domain_app_folder)))
#            logging.error("os.path.abspath('.') = "+os.path.abspath("."))
            os.makedirs(domain_app_folder)
            shutil.copy(default_jr_path,domain_app_folder)
            shutil.copy(default_jad_path,domain_app_folder)
            uri = domain_app_jar_path
        jar = JarDownloadItem(uri=uri,name="JavaRosa")
        jar.description = "Domain Specific JavaRosa client automatically added for domain: "+str(domain)+", from path: "+uri
        jar.version = findParamInfo(domain_app_jad_path,"App-Version")
        
        
        if domain == "default":
            jar.default_version = True
        else:
            jar.domain = Domain.objects.get(name__iexact=domain)
            jar.default_version = False
        jar.save()
    else:
        jar = jars[0]
        
    return jar

#def find_or_create_default_jar():
#    jars = JarDownloadItem.objects.filter(jad__is_original=True)
#    if len(jars) == 0:
#        default_jr_path = settings.JAVAROSA_DEFAULT_JAR_PATH
#        if not os.path.exists(default_jr_path):
#            raise Exception("JAVAROSA DEFAULT JAR NOT FOUND!")
#            return False
#        
#        domain_app_folder = os.path.join(settings.UPLOADED_APP_STORAGE_PATH,"default")
#        
#        #if jar for this DEFAULT jar doesn't exist in the uploaded apps folder
#        #copy the default jar into apps/default and use that.
#        if os.path.exists(domain_app_folder):
#            shutil.copy(default_jr_path,domain_app_folder)
#            uri = os.path.join(domain_app_folder,os.path.basename(default_jr_path))
#        else:
#            os.makedirs(domain_app_folder)
#            shutil.copy(default_jr_path,domain_app_folder)
#            uri = os.path.join(domain_app_folder,os.path.basename(default_jr_path))
#        jar = JarDownloadItem(uri=uri,name="JavaRosa Default Version")
#        jar.description = "Base JavaRosa client automatically added to database from path: "+uri
#        jar.version = findParamInfo(uri.replace(".jar",".jad"),"App-Version") #there should always be an accompanying jad file
#        jar.save()
#    else:
#        jar = jars[0]
#        
#    return jar

#def find_or_create_default_jad():
#    jads = JadDownloadItem.objects.filter(is_original=True)
#    
#    default_jr_path = settings.JAVAROSA_DEFAULT_JAR_PATH
#    domain_app_folder = os.path.join(settings.UPLOADED_APP_STORAGE_PATH,"default")
#    jad_file_loc = os.path.join(domain_app_folder,os.path.basename(default_jr_path).replace(".jar",".jad"))
#    jar = find_or_create_default_jar()
#
#    
#    if not os.path.exists(jad_file_loc):
#        if os.path.exists(os.path.dirname(jad_file_loc)):
#            shutil.copy(default_jr_path.replace(".jar",".jad"),jad_file_loc)
#        else:
#            #something is horribly wrong
#            raise Exception("Attempted to create Jad with no accompanying Jar in downloads.utils.find_or_create_domain")
#    
#    if len(jads) == 0:
#        uri = jar.uri.replace(".jar",".jad")
#        
#        #create the new model entry
#        jad = JadDownloadItem(uri=uri,jar=jar,is_original=False)
#        jad.version = findParamInfo(uri.replace(".jar",".jad"),"App-Version")
#        jad.description = "Auto Generated Jad for default domain"
#        midlet_url = settings.DATAHQ_URL+"/download/jar"
#        set_midlet_url(jad_file_loc, midlet_url)
#        jad.midlet_url = midlet_url
#        
#        post_url = settings.JAVAROSA_DEFAULT_POST_URL
#        set_JRDemo_Post_Url(jad_file_loc, post_url)
#        jad.form_post_url = post_url
#        
#        form_list_url = settings.JAVAROSA_DEFAULT_FORM_LIST_URL
#        set_JRDemo_Post_Url_List(jad_file_loc, form_list_url)
#        jad.form_list_url = form_list_url
#        
#        jad.save()
#    else:
#        jad = jads[0]
#        
#    return jad


def get_contents(downloadItem):
        """Get the contents for an attachment object, by reading (fully) the
           underlying file."""
        fin = None
        try:
            fin = open(downloadItem.uri ,'r')
            return fin.read()
        except Exception, e:
            logging.error("Unable to open downloadItem %s. %s" % (downloadItem, e.message),
                          extra={"exception": e})
        finally:
            if fin:   fin.close()
