import os
import sys
import cherrypy
from cherrypy import wsgiserver
import logging

filedir = os.path.dirname(__file__)
sys.path.append(os.path.join(filedir,'..'))
sys.path.append(os.path.join(filedir,'..', '..'))
sys.path.append(os.path.join(filedir,'..','apps'))
sys.path.append(os.path.join(filedir,'..', 'care_apps'))
sys.path.append(os.path.join(filedir,'..', 'shared_code'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'datahq.settings'

wsgiserver.CherryPyWSGIServer.ssl_certificate = "/home/dmyung/self_ssl/cert/server.crt"
wsgiserver.CherryPyWSGIServer.ssl_private_key = "/home/dmyung/self_ssl/cert/server.key"


import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

server = wsgiserver.CherryPyWSGIServer(
    ('0.0.0.0', 443),  # Use '127.0.0.1' to only bind to the localhost
    django.core.handlers.wsgi.WSGIHandler()
)

try:        
    
    logging.info("Starting server runtime...")
    server.start()                        
except KeyboardInterrupt:
    logging.info("Keyboard interrupt, shutting down server")
    logging.info("server shutdown successful")

