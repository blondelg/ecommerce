"""
Django settings for ecommerce project.
"""

import os
import configparser
from oscar.defaults import *
from django.utils.translation import gettext_lazy as _


# Load config
config = configparser.ConfigParser()
config.read('ecommerce/settings/config.ini')

# Useful paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONTENT_DIR = os.path.join(BASE_DIR, 'apps_custom', 'content')

# Basic configs
DEBUG = True
if config['CONFIG']['DEBUG'].strip() in ['False', 'false', 'FALSE']: DEBUG = False

SECRET_KEY = config['CONFIG']['SECRET_KEY']

INTERNAL_IPS = config['CONFIG']['INTERNAL_IPS'].split(",")

ALLOWED_HOSTS = config['CONFIG']['ALLOWED_HOSTS'].split(",")


# Database
DATABASES = {
    'default': {
        'ENGINE': config['DATABASE']['ENGINE'],
        'NAME': config['DATABASE']['NAME'],
        'USER': config['DATABASE']['USER'],
        'PASSWORD': config['DATABASE']['PASSWORD'],
        'HOST': config['DATABASE']['HOST'],
        'PORT': config['DATABASE']['PORT'],
    }
}

# Application definition
DEFAULT_APPS = [

    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',
]

THIRD_PARTY_APPS = [

    # Wagtail
    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.contrib.modeladmin',
    'wagtail.contrib.settings',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',

    # Oscar
    'oscar',
    'oscar.apps.address',
    'oscar.apps.catalogue.reviews',
    'oscar.apps.payment',
    'oscar.apps.offer',
    'oscar.apps.search',
    'oscar.apps.voucher',
    'oscar.apps.wishlists',
    'oscar.apps.dashboard.users',
    'oscar.apps.dashboard.offers',
    'oscar.apps.dashboard.partners',
    'oscar.apps.dashboard.pages',
    'oscar.apps.dashboard.ranges',
    'oscar.apps.dashboard.reviews',
    'oscar.apps.dashboard.vouchers',
    'oscar.apps.dashboard.communications',

    
    # 3rd-party apps that oscar depends on
    'widget_tweaks',
    'haystack',
    'treebeard',
    'sorl.thumbnail',
    'django_tables2',
    'taggit',
    'modelcluster',

    # chartjs
    'chartjs',
]

LOCAL_APPS = [

    # Oscar forked
    'apps_fork.analytics.apps.AnalyticsConfig',
    'apps_fork.checkout.apps.CheckoutConfig',
    'apps_fork.shipping.apps.ShippingConfig',
    'apps_fork.catalogue.apps.CatalogueConfig',
    'apps_fork.partner.apps.PartnerConfig',
    'apps_fork.basket.apps.BasketConfig',
    'apps_fork.order.apps.OrderConfig',
    'apps_fork.customer.apps.CustomerConfig',
    'apps_fork.dashboard.apps.DashboardConfig',
    'apps_fork.dashboard.reports.apps.ReportsDashboardConfig',
    'apps_fork.dashboard.orders.apps.OrdersDashboardConfig',
    'apps_fork.dashboard.catalogue.apps.CatalogueDashboardConfig',
    'apps_fork.dashboard.shipping',
    'apps_fork.dashboard.donation.apps.DonationDashboardConfig',

    # Home made
    'apps_custom.datavisu',
    'apps_custom.content',
    'apps_custom.settings',
]

INSTALLED_APPS = DEFAULT_APPS + THIRD_PARTY_APPS + LOCAL_APPS

SITE_ID = 1

MIDDLEWARE = [
    
    # Django
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'oscar.apps.basket.middleware.BasketMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    
    # Wagtail
    'wagtail.core.middleware.SiteMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]

ROOT_URLCONF = 'ecommerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(CONTENT_DIR, 'templates'),

        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'oscar.apps.search.context_processors.search_form',
                'oscar.apps.checkout.context_processors.checkout',
                'oscar.apps.customer.notifications.context_processors.notifications',
                'oscar.core.context_processors.metadata',
                'wagtail.contrib.settings.context_processors.settings',
            ],
        },
    },

]

WSGI_APPLICATION = 'ecommerce.wsgi.application'

# Oscar authentification
AUTHENTICATION_BACKENDS = (
    'oscar.apps.customer.auth_backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
)


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'fr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

gettext_noop = lambda s: s
LANGUAGES = (
    ('da', gettext_noop('Danish')),
    ('de', gettext_noop('German')),
    ('en', gettext_noop('English')),
    ('el', gettext_noop('Greek')),
    ('es', gettext_noop('Spanish')),
    ('fi', gettext_noop('Finnish')),
    ('fr', gettext_noop('French')),
    ('it', gettext_noop('Italian')),
    ('nl', gettext_noop('Dutch')),
    ('pt', gettext_noop('Portuguese')),
)


# Media
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Statics
STATIC_ROOT = os.path.join(BASE_DIR, 'staticroot')
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'staticfiles')]

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}

# OTHER SETTINGS ########################################
CSV_MAX_SIZE = 1 # in Mo
CSV_ROOT = ''

# Content settings
WAGTAIL_SITE_NAME = 'content tautoko'

# Oscars settings
OSCAR_DEFAULT_CURRENCY = 'EUR'

OSCAR_SHOP_NAME = 'Tautoko'

OSCAR_FROM_EMAIL = 'tautokoteam@gmail.com'
OSCAR_SEND_REGISTRATION_EMAIL = True
# order pipeline

OSCAR_INITIAL_LINE_STATUS = 'Pending'
OSCAR_LINE_STATUS_PIPELINE = {
    'Pending': ('Being processed', 'Cancelled',),
    'Being processed': ('Processed', 'Cancelled',),
    'Processed': (),
    'Cancelled': (),
}

OSCAR_INITIAL_ORDER_STATUS = 'Pending'
OSCAR_ORDER_STATUS_PIPELINE = {
    'Pending': ('Being processed', 'Cancelled',),
    'Being processed': ('Processed', 'Cancelled',),
    'Cancelled': (),
}



# Dashboard navigation
from ecommerce.settings.dashboard_menus import OSCAR_DASHBOARD_NAVIGATION

# Tax
OSCAR_DEFAULT_TAX_RATE = 0.196
OSCAR_OFFERS_INCL_TAX = True

# Google analytics
OSCAR_GOOGLE_ANALYTICS_ID = ''

#Additional configs loaded to link urls which are outside of the dashboard scope
OSCAR_CONFIG_DASHBOARD = ['wagtail.admin']

# Rate of donation as per cent of revenues
TAUTOKO_RATE_OF_DONATION = 0.05
