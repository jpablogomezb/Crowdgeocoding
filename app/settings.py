# -*- encoding: utf-8 -*-
"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from decouple import config, Csv
#GEOS_LIBRARY_PATH=config('GEOS_LIBRARY_PATH')
#GDAL_LIBRARY_PATH=config('GDAL_LIBRARY_PATH')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', cast=str)
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())
#Email Delivery Service (E.g. SendGrid Account) 
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_MAIN = config('EMAIL_MAIN')
EMAIL_PLATFORM = config('EMAIL_PLATFORM')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.gis',
    'leaflet',
    'app',
    'map',
    'tasks',
    'contact',
    'crispy_forms',
    'allauth',
    'allauth.account',
)

SITE_ID = 1

CRISPY_TEMPLATE_PACK = 'bootstrap3'

LOGIN_URL ='/accounts/login/'
LOGIN_REDIRECT_URL = '/my-profile/'

ACCOUNT_AUTHENTICATION_METHOD = "username_email" #(="username" | "email" | "username_email")
ACCOUNT_CONFIRM_EMAIL_ON_GET = False # (=False)
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL =  LOGIN_URL
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = LOGIN_REDIRECT_URL
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 10
ACCOUNT_EMAIL_REQUIRED = True 
ACCOUNT_EMAIL_VERIFICATION = "optional" #choices are: "mandatory", "optional", or None
ACCOUNT_EMAIL_SUBJECT_PREFIX = "Crowd-Geocoding: "
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "http" #if secure use https
ACCOUNT_LOGOUT_ON_GET = False #log user out right away.
ACCOUNT_LOGOUT_REDIRECT_URL = LOGIN_URL
ACCOUNT_SIGNUP_FORM_CLASS = None # add a custom sign up form
ACCOUNT_SIGNUP_PASSWORD_VERIFICATION =True # use False if you don't want double password fields
ACCOUNT_UNIQUE_EMAIL= True #enforces emails are unique to all accounts
ACCOUNT_USER_MODEL_USERNAME_FIELD = "username" # If you're using a Custom Model, maybe it's "email"
ACCOUNT_USER_MODEL_EMAIL_FIELD = "email" 
#ACCOUNT_USER_DISPLAY (=a callable returning user.username)
ACCOUNT_USERNAME_MIN_LENGTH = 4
#ACCOUNT_USERNAME_BLACKLIST =['']
ACCOUNT_USERNAME_REQUIRED = True #do you want them to have a user name?
ACCOUNT_PASSWORD_INPUT_RENDER_VALUE =False #don't show the password
ACCOUNT_PASSWORD_MIN_LENGTH = 6 #min length of password
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION =True #login the user after confirming email, if required.

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [

                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                # allauth specific context processors
                "allauth.account.context_processors.account",
                "allauth.socialaccount.context_processors.socialaccount",
                
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'

GOOGLE_API = config('GOOGLE_API', cast=str)
BING_API = config('BING_API', cast=str)
#HERE_APP_CODE = config('HERE_APP_CODE', cast=str)
#HERE_APP_ID = config('HERE_APP_ID', cast=str)
MAPBOX_API = config('MAPBOX_API', cast=str)
MAPQUEST_API = config('MAPQUEST_API', cast=str)

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.mysql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': '',
        'OPTIONS': {
            'sql_mode': 'traditional',
            'init_command': 'SET foreign_key_checks = 0;',
        },
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.contrib.gis.db.backends.spatialite', #libspatialite installation is needed... 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'), 
#     }
# }

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
    )


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/
from django.utils.translation import ugettext_lazy as _
LANGUAGES = (
    ('en', _('English')),
    ('es', _('Espa??ol')),
)

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Universal'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = False

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

MEDIA_URL = "/media/"

MEDIA_ROOT = os.path.join(BASE_DIR, "static", "media")

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, "static", "root")

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static", "static"),
)

# Locale paths
# ------------
# Help Django find any translation files.

LOCALE_PATHS = (
    os.path.join(BASE_DIR, "static", "locale"),
    os.path.join(BASE_DIR, "locale"),
)

