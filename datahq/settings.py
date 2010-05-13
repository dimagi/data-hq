# Django settings for datahq project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'    # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'datahq.db'    # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/static'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'fixme'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'domain.middleware.DomainMiddleware',
)

ROOT_URLCONF = 'datahq.urls'


TEMPLATE_CONTEXT_PROCESSORS = [
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "context_processors.base_template" # sticks the base template inside all responses
]


DEFAULT_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    
)

HQ_APPS = (
    'django_granular_permissions',
    'django_rest_interface',
    'datahq.apps.django_tables',
    'datahq.apps.user_registration',
    'datahq.apps.domain',
    'datahq.apps.receiver',
    'datahq.apps.xformmanager',
    'datahq.apps.hqwebapp'
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = DEFAULT_APPS + HQ_APPS

# CZUE:  these have been added as new custom properties to the settings
# and are migrated from the previous rapidsms framework

####### Receiver Settings #######
RECEIVER_SUBMISSION_PATH="data/submissions"
RECEIVER_ATTACHMENT_PATH="data/attachments"
RECEIVER_EXPORT_PATH="data"

####### XFormManager Settings #######
XFORMMANAGER_SCHEMA_PATH="data/schemas"
XFORMMANAGER_EXPORT_PATH="data"
XFORMMANAGER_FORM_TRANSLATE_JAR="lib/form_translate.jar"


####### Domain settings  #######

DOMAIN_MAX_REGISTRATION_REQUESTS_PER_DAY=99
DOMAIN_SELECT_URL="/domain/select/"
LOGIN_URL="/accounts/login/"
# For the registration app
# One week to confirm a registered user account
ACCOUNT_ACTIVATION_DAYS=7 
# If a user tries to access domain admin pages but isn't a domain 
# administrator, here's where he/she is redirected
DOMAIN_NOT_ADMIN_REDIRECT_PAGE_NAME="homepage"


####### Shared/Global/UI Settings ######

# restyle some templates
BASE_TEMPLATE="hq-layout.html"
LOGIN_TEMPLATE="login_and_password/login.html"
LOGGEDOUT_TEMPLATE="loggedout.html"



# email settings: these ones are the custom hq ones
EMAIL_LOGIN="user@domain.org"
EMAIL_PASSWORD="changeme"
EMAIL_SMTP_HOST="smtp.gmail.com"
EMAIL_SMTP_PORT=587

# these are the official django settings
# which really we should be using over the
# above
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "user@domain.org"
EMAIL_HOST_PASSWORD = "changeme"
EMAIL_USE_TLS = True


TABS = [
    ('hqwebapp.views.dashboard', 'Dashboard'),
    ('xformmanager.views.dashboard', 'XForms'),
    ('receiver.views.show_submits', 'Submissions'),
]

# import local settings if we find them
try:
    from localsettings import *
except ImportError:
    pass
