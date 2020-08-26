"""
Django settings for ecommerce project.
"""

import os
import configparser
from oscar.defaults import *
from django.utils.translation import gettext_lazy as _
from .base import *  # noqa

# Email setup
EMAIL_SUBJECT_PREFIX = '[Tautoko] '
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Applicatio definition
INSTALLED_APPS += [

    # for jupyter
    'django_extensions',

    # debug
    'debug_toolbar',

]

MIDDLEWARE += [

    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

DEBUG_TOOLBAR_CONFIG = {
    'DISABLE_PANELS': [
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ],
    'SHOW_TEMPLATE_CONTEXT': True,
}
