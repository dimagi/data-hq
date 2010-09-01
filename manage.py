#!/usr/bin/env python
from django.core.management import execute_manager
import sys, os

# add our local apps and shared directory to the path for convenience
filedir = os.path.dirname(__file__)
sys.path.append(filedir)
"""sys.path.append(os.path.join(filedir,'corehq'))
sys.path.append(os.path.join(filedir,'corehq','apps'))
sys.path.append(os.path.join(filedir,'corehq','lib'))
sys.path.append(os.path.join(filedir,'corehq','util'))
"""
sys.path.append(os.path.join(filedir,'care_apps'))

try:
    import settings # Assumed to be in the same directory.
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
    sys.exit(1)

if __name__ == "__main__":
    execute_manager(settings)
