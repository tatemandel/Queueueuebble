"""
Django settings for queueuebble project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

STATIC_URL = '/static/'

STATICFILES_DIRS = (
        # Put strings here, like "/home/html/static" or "C:/www/django/static".
        # Always use forward slashes, even on Windows.
        # Don't forget to use absolute paths, not relative paths.
        os.path.join(
            os.path.dirname(__file__),
            'static',
            ),
        )

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6gbmeayf_!z0e#ildvxtj_0n_=lh$9=5nv5ymc(s3&#%5qx_85'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

LOGIN_URL = '/login/'

LOGOUT_URL = '/logout/'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'queue',
    'south',
    'twitter_bootstrap'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'queueuebble.urls'

WSGI_APPLICATION = 'queueuebble.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'QueueDB',
        'USER': 'queue_admin',
        'PASSWORD': 'queue-password',
        'HOST': 'queue-db.cdgszcte87bu.us-east-1.rds.amazonaws.com',
        'PORT': '1512'
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'queueuebble',
#         'USER': 'queue_admin',
#         'PASSWORD': 'abc123'

#    }
# }

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

#Email user

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'QQQ'
EMAIL_HOST_PASSWORD = 'qqqq1234'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

TEMPLATE_DIRS = (
        'templates'
        )
