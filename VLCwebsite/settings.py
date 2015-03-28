"""
Django settings for VLCwebsite project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = 'y^#gaaox+2pn71-7v#eofd(&#bi+7s3kp=yy#p=1n=oj1@4uac'
with open('c:/Users/i7-2600K/DjangoProjects/secret_key.txt') as f:
    SECRET_KEY = f.read().strip()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'vinlacvicek.ddns.net', 'www.vinlacvicek.com', 'vinlacvicek.com']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'home',
    'pybb.apps.PybbConfig',
    'pytils',
    'pure_pagination',
    'account',
    'pinax_theme_bootstrap',
    'bootstrapform',
    'captcha',
    'compressor'
)

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates'),
                 'C:/Users/i7-2600K/DjangoProjects/VLCwebsite/home/templates',
                 'C:/Python34/Lib/site-packages/pybb/templates',]

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)



MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'account.middleware.LocaleMiddleware',
    'account.middleware.TimezoneMiddleware',
    'pybb.middleware.PybbMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    "account.context_processors.account",
    'django.core.context_processors.request',
    'pinax_theme_bootstrap.context_processors.theme',
    'pybb.context_processors.processor',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.debug',
)

#AUTH_PROFILE_MODULE = 'accounts.UserProfile'
AUTH_PROFILE_MODULE = 'pybb.Profile'

ROOT_URLCONF = 'VLCwebsite.urls'

WSGI_APPLICATION = 'VLCwebsite.wsgi.application'

ADMINS = (('Jernej', 'jernej.mrvar@gmail.com'),('Admin', 'admin@vinlacvicek.com'))

MANAGERS = (('Jernej', 'jernej.mrvar@gmail.com'),('Admin', 'admin@vinlacvicek.com'))

#ADMINS =(('Jernej', 'jernej.mrvar@gmail.com'),)
#MANAGERS =(('Jernej', 'jernej.mrvar@gmail.com'),)

#ADMINS = (('admin', 'admin@vinlacvicek.com'),)
#MANAGERS = (('admin', 'admin@vinlacvicek.com'),)


#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'

#EMAIL_USE_SSL = True    #port 465

#Google
#EMAIL_USE_TLS = True   #port 587
#EMAIL_HOST = 'smtp.gmail.com'
#EMAIL_HOST_USER = 'vinlacvicek@gmail.com'
#EMAIL_HOST_PASSWORD = 'fqhsqklzkzxzelth'
#EMAIL_PORT = 587


DEFAULT_FROM_EMAIL = 'Vin la Cvicek <admin@vinlacvicek.com>'
SERVER_EMAIL = 'admin@vinlacvicek.com'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.zoho.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'admin@vinlacvicek.com'
EMAIL_HOST_PASSWORD = '6b2gbmk8wsqz'



SITE_ID = 9

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

ENV_PATH = os.path.abspath(os.path.dirname(__file__))
MEDIA_ROOT = os.path.join(ENV_PATH, 'media/')


#MEDIA_URL = 'assets/'
MEDIA_URL = '/media/'

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'CET'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

#STATIC_ROOT = os.path.join(PROJECT_ROOT, '/static/')
#STATIC_ROOT = os.path.join(BASE_DIR, "/static/")
STATIC_ROOT = 'staticfiles'

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

#account
THEME_CONTACT_EMAIL = 'admin@vinlacvicek.com'

#forum
PYBB_DEFAULT_AUTOSUBSCRIBE = False
PYBB_ENABLE_ANONYMOUS_POST = False
PYBB_DEFAULT_TITLE = "Forum"
PYBB_ANONYMOUS_USERNAME = "Annonymous"
PYBB_ATTACHMENT_ENABLE = False
PYBB_TEMPLATE = "site_base.html"
PYBB_SMILES_PREFIX = "emoticons/"
PYBB_DEFAULT_TIME_ZONE = 3
PYBB_SMILES = {
    ':(': 'sad.gif',
    ':D': 'biggrin.gif',
    ':P': 'tongue.gif',
    ':o': 'ohmy.gif',
    '*happyno*': 'happyno.gif',
    'oO': 'huh.gif',
    'o_O': 'blink.gif',
    '<.<': 'dry.gif',
    '8)': 'cool.gif',
    'ˇˇ': 'goodgrief.gif',
    '*mad*': 'mad.gif',
    '*lol*': 'laugh.gif',
    '*mellow*': 'mellow.gif',
    '*sadno*': 'sadno.gif',
    '*^^*': 'smug.gif',
    '*unsure*': 'unsure.gif',
    ';)': 'wink.gif',
    ':)': 'smile.gif',
    '*zzz*': 'sleep.gif',
}

PYBB_MARKUP_ENGINES_PATHS ={'bbcode': 'pybb.markup.markup_engines.CustomBBCodeParser'}
PYBB_MARKUP = 'bbcode'