"""
Django settings for ecommerce project.
"""

import os
import environ
from oscar.defaults import *
from django.utils.translation import gettext_lazy as _

env = environ.Env()

# Path helper
location = lambda x: os.path.join(
    os.path.dirname(os.path.realpath(__file__)), x)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT_DIR = os.path.join(BASE_DIR, 'apps_custom', 'content')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '95)+qd1%!g#_g@!2op+nipk^3eu&c2-$l*v6i3z49bjy9rucd2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['ec2-35-180-98-235.eu-west-3.compute.amazonaws.com', 'localhost', '127.0.0.1']
#ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])

INTERNAL_IPS = [
    '127.0.0.1',
]

EMAIL_SUBJECT_PREFIX = '[Tautoko] '
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "@gmail.com"
EMAIL_HOST_PASSWORD = ""
# EMAIL_USE_SSL = True
EMAIL_USE_TLS = True

# Applicatio definition

INSTALLED_APPS = [

    # Wagtail
    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',
    'wagtail.contrib.modeladmin',
    
    'taggit',
    'modelcluster',

    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',

    # Oscar
    'oscar',

    #'oscar.apps.analytics',
    'apps_fork.analytics.apps.AnalyticsConfig',

    #'oscar.apps.checkout',
    'apps_fork.checkout.apps.CheckoutConfig',

    'oscar.apps.address',
    #'oscar.apps.shipping',
    'apps_fork.shipping.apps.ShippingConfig',

    #'oscar.apps.catalogue',
    'apps_fork.catalogue.apps.CatalogueConfig',

    'oscar.apps.catalogue.reviews',

    #'oscar.apps.partner',
    'apps_fork.partner.apps.PartnerConfig',

    #'oscar.apps.basket',
    'apps_fork.basket.apps.BasketConfig',
    'oscar.apps.payment',
    'oscar.apps.offer',

    #'oscar.apps.order',
    'apps_fork.order.apps.OrderConfig',

    #'oscar.apps.customer',
    'apps_fork.customer.apps.CustomerConfig',

    'oscar.apps.search',
    'oscar.apps.voucher',
    'oscar.apps.wishlists',

    #'oscar.apps.dashboard',
    'apps_fork.dashboard.apps.DashboardConfig',

    #'oscar.apps.dashboard.reports',
    'apps_fork.dashboard.reports.apps.ReportsDashboardConfig',

    'oscar.apps.dashboard.users',

    # 'oscar.apps.dashboard.orders',
    'apps_fork.dashboard.orders.apps.OrdersDashboardConfig',

    #'oscar.apps.dashboard.catalogue',
    'apps_fork.dashboard.catalogue.apps.CatalogueDashboardConfig',

    'oscar.apps.dashboard.offers',
    'oscar.apps.dashboard.partners',
    'oscar.apps.dashboard.pages',
    'oscar.apps.dashboard.ranges',
    'oscar.apps.dashboard.reviews',
    'oscar.apps.dashboard.vouchers',
    'oscar.apps.dashboard.communications',

    #'oscar.apps.dashboard.shipping',
    'apps_fork.dashboard.shipping',
    
    # Not a fork of existing app but make sense to have it in dashboard
    'apps_fork.dashboard.donation.apps.DonationDashboardConfig',

    # 3rd-party apps that oscar depends on
    'widget_tweaks',
    'haystack',
    'treebeard',
    'sorl.thumbnail',
    'django_tables2',

    # for jupyter
    'django_extensions',

    # Apps
    'apps_custom.datavisu',
    'apps_custom.content',

    # debug
    'debug_toolbar',

    # chartjs
    'chartjs',
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'oscar.apps.basket.middleware.BasketMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',

    'wagtail.core.middleware.SiteMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',


    'debug_toolbar.middleware.DebugToolbarMiddleware',
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

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


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

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

# setup directories
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


STATIC_ROOT = os.path.join(BASE_DIR, 'staticroot')
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'staticfiles')]

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}

# in-house app settings
CSV_MAX_SIZE = 1 # in Mo
CSV_ROOT = location("public/csv")


# Content settings
WAGTAIL_SITE_NAME = 'content tautoko'


# Oscars settings
OSCAR_DEFAULT_CURRENCY = 'EUR'

OSCAR_SHOP_NAME = 'Tautoko'

OSCAR_FROM_EMAIL = 'geoffroy.blondel@gmail.com'
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

def partner_access(user, y, z, a):
    #print(user.groups)
    return True

OSCAR_DASHBOARD_NAVIGATION = [
{'label': 'Dashboard', 'icon': 'fas fa-chart-line', 'url_name': 'dashboard:index'},
{'label': 'Products', 'icon': 'fas fa-store', 'url_name': 'dashboard:catalogue-product-list'},
{'label': 'Orders', 'icon': 'fas fa-shopping-cart', 'url_name': 'dashboard:order-list'},
{'label': 'Donations', 'icon': 'fas fa-donate', 'url_name': 'dashboard:donation-list'},
{'label': 'Customers', 'icon': 'fas fa-users', 'url_name': 'dashboard:users-index', 'access_fn': partner_access},
{'label': 'Shipping', 'icon': 'fas fa-truck', 'url_name': 'dashboard:shipping-method-list', 'access_fn': partner_access},
{'label': 'Low stock alerts', 'icon': 'fas fa-exclamation-circle', 'url_name': 'dashboard:stock-alert-list', 'access_fn': partner_access},
{'label': 'Reviews', 'icon': 'fas fa-thumbs-up', 'url_name': 'dashboard:reviews-list', 'access_fn': partner_access},
{'label': 'Content Admin', 'icon': 'far fa-newspaper', 'url_name': 'wagtailadmin_home', 'access_fn': partner_access},
{'label': 'Data',  'icon': 'fas fa-file-csv', 'url_name': 'dashboard:reports-index'},
{'label': 'Analytics',  'icon': 'fas fa-chart-bar', 'staff': 'True', 'url_name': 'dashboard:reports-index'},


{'label': 'Settings', 'icon': 'fas fa-cogs', 'staff': 'True', 'children': [
{'label': 'Partners', 'url_name': 'dashboard:partner-list'},
{'label': 'Product Types', 'url_name': 'dashboard:catalogue-class-list'},
{'label': 'Product Categories', 'url_name': 'dashboard:catalogue-category-list'},
{'label': 'Product Ranges', 'url_name': 'dashboard:range-list'},
{'label': 'Stock alert', 'url_name': 'dashboard:user-alert-list'},
{'label': 'Product Options', 'url_name': 'dashboard:catalogue-option-list'},
{'label': 'Offers', 'url_name': 'dashboard:offer-list'},
{'label': 'Coupons', 'url_name': 'dashboard:voucher-list'},
{'label': 'Voucher Sets', 'url_name': 'dashboard:voucher-set-list'},
{'label': 'Pages', 'url_name': 'dashboard:page-list'},
{'label': 'Email templates', 'url_name': 'dashboard:comms-list'},
{'label': 'Visualisation', 'url_name': 'dashboard:datavisu'},
{'label': 'Statistics', 'url_name': 'dashboard:order-stats'},
]},]

OSCAR_DEFAULT_TAX_RATE = 0.196
OSCAR_OFFERS_INCL_TAX = True

OSCAR_GOOGLE_ANALYTICS_ID = ''

#Additional configs loaded to link urls which are outside of the dashboard scope
OSCAR_CONFIG_DASHBOARD = ['wagtail.admin']

# Rate of donation as per cent of revenues
TAUTOKO_RATE_OF_DONATION = 0.05
