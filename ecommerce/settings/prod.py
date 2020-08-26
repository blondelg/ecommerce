"""
Django settings for ecommerce project.
"""

import os
import configparser
from oscar.defaults import *
from django.utils.translation import gettext_lazy as _
from .base import *  # noqa

# Email settings
EMAIL_SUBJECT_PREFIX = config['EMAIL']['EMAIL_SUBJECT_PREFIX']
EMAIL_BACKEND = config['EMAIL']['EMAIL_BACKEND']
EMAIL_HOST = config['EMAIL']['EMAIL_HOST']
EMAIL_PORT = config['EMAIL']['EMAIL_PORT']
EMAIL_HOST_USER = config['EMAIL']['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = config['EMAIL']['EMAIL_HOST_PASSWORD']
EMAIL_USE_TLS = config['EMAIL']['EMAIL_USE_TLS']
