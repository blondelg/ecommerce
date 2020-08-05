"""
Django settings for ecommerce project.
"""

import os
import environ
from oscar.defaults import *
from django.utils.translation import gettext_lazy as _
from .base import *  # noqa

env = environ.Env()



# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['']


EMAIL_SUBJECT_PREFIX = '[Tautoko] '
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "@gmail.com"
EMAIL_HOST_PASSWORD = ""
# EMAIL_USE_SSL = True
EMAIL_USE_TLS = True


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.',
        'NAME': ,
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

