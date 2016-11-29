"""
Django settings for srtstorage project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from private_settings import MY_ADMIN_MEDIA_PREFIX, MY_SECRET_KEY, MY_DEBUG, MY_TEMPLATE_DEBUG, MY_ALLOWED_HOSTS, \
    MY_ROOT_URLCONF, MY_WSGI_APPLICATION, MY_TEMPLATE_DIRS, MY_STATICFILES_DIRS, MY_DATABASES, MY_STATIC_URL, \
    MY_STORAGE_FOLDER, MY_RECAPTCHA_PUBLIC_KEY, MY_RECAPTCHA_PRIVATE_KEY

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

ADMIN_MEDIA_PREFIX = MY_ADMIN_MEDIA_PREFIX

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = MY_SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = MY_DEBUG

TEMPLATE_DEBUG = MY_TEMPLATE_DEBUG

ALLOWED_HOSTS = MY_ALLOWED_HOSTS

# Application definition

INSTALLED_APPS = (
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    # 'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_tables2',
    # 'pure_pagination',
    "captcha",
    'dajaxice',
    "storage",
)

PAGINATION_SETTINGS = {
    'PAGE_RANGE_DISPLAYED': 10,
    'MARGIN_PAGES_DISPLAYED': 2,
}

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = MY_ROOT_URLCONF

WSGI_APPLICATION = MY_WSGI_APPLICATION

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
)

TEMPLATE_DIRS = MY_TEMPLATE_DIRS

STATICFILES_DIRS = MY_STATICFILES_DIRS

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'dajaxice.finders.DajaxiceFinder',
)

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = MY_DATABASES

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = MY_STATIC_URL

STORAGE_FOLDER = MY_STORAGE_FOLDER

RECAPTCHA_PUBLIC_KEY = MY_RECAPTCHA_PUBLIC_KEY

RECAPTCHA_PRIVATE_KEY = MY_RECAPTCHA_PRIVATE_KEY
