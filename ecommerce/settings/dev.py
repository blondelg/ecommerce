"""
Django settings for ecommerce project.
"""

import os
import environ
from oscar.defaults import *
from django.utils.translation import gettext_lazy as _
from .base import *  # noqa

env = environ.Env()

# Path helper
location = lambda x: os.path.join(
    os.path.dirname(os.path.realpath(__file__)), x)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT_DIR = os.path.join(BASE_DIR, 'apps_custom', 'content')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '95)+qd1%!g#_g@!2op+nipk^3eu&c2-$l*v6i3z49bjy9rucd2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['ec2-35-180-98-235.eu-west-3.compute.amazonaws.com', 'localhost', '127.0.0.1']


INTERNAL_IPS = [
    '127.0.0.1',
]

EMAIL_SUBJECT_PREFIX = '[Tautoko] '
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "@gmail.com"
EMAIL_HOST_PASSWORD = ""
EMAIL_USE_TLS = True

# Applicatio definition

INSTALLED_APPS += [

    # for jupyter
    'django_extensions',

    # debug
    'debug_toolbar',

]

SITE_ID = 1

MIDDLEWARE += [

    'debug_toolbar.middleware.DebugToolbarMiddleware',
]


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

DEBUG_TOOLBAR_CONFIG = {
    'DISABLE_PANELS': [
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ],
    'SHOW_TEMPLATE_CONTEXT': True,
}
