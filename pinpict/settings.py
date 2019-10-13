"""
Django settings for pinpict project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import datetime

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Previews generation settings
# JPEG quality shouldn't be more than 95 and less than 50.
# 90 for big previews and 70 for small ones are a good value.

# (width, destination folder relative to PREVIEWS_ROOT, and JPEG quality
PREVIEWS_WIDTH = [
        (736, '736', 90),
        (236, '236', 70),
]

# previews with given width and height
# (width, height, destination folder relative to PREVIEWS_ROOT, and JPEG quality
PREVIEWS_CROP = [
        (216, 160, '216-160', 70),
        (50, 50, '50', 70),
]

# words that can't be used as username
RESERVED_WORDS = (
        'admin',
        'board',
        'pin',
        'login',
        'logout',
        'profil',
        'register',
        'signup',
        'signin',
        'recovery',
        'page',
        'user',
        'notifications',
)

# words that can't be used as board name
BOARD_RESERVED_WORDS = (
        'pins',
        'page',
        'followers',
        'following',
)

# max size for avatar img (side in px)
# if uploaded file is bigger, it will be resized.
AVATAR_MAX_SIZE = 150

# search engine configuration
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
    },
}

## HEADERS
# allow CORS from everywhere
CORS_ORIGIN_ALLOW_ALL = False


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sitemaps',
    'rest_framework',
    'debug_toolbar',
    'user',
    'board',
    'pin',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware', # comment for prod
)

ROOT_URLCONF = 'pinpict.urls'

WSGI_APPLICATION = 'pinpict.wsgi.application'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
    		os.path.join(BASE_DIR, 'templates/'),
	],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.media",
            ],
        },
    },
]
# To add slash at url ends
APPEND_SLASH = True

## users abstract model
AUTH_USER_MODEL = 'user.User'

## login page
LOGIN_URL = '/login/'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/
DEFAULT_CHARSET = 'utf-8'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_ROOT = ''
STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'pinpict/assets-root')
STATICFILES_DIRS = (
        os.path.join(BASE_DIR, 'pinpict/assets/'),
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'pinpict/data/')

PREVIEWS_ROOT = os.path.join(MEDIA_ROOT, 'previews')

MEDIA_URL = '/media/'

STATICFILES_FINDERS = ("django.contrib.staticfiles.finders.FileSystemFinder",
 "django.contrib.staticfiles.finders.AppDirectoriesFinder")



REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAdminUser',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication', # for api with header
        'user.authentication.JSONWebTokenAuthenticationCookie', # for api with cookie
        'rest_framework.authentication.SessionAuthentication', # for django rest framework browser
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 200,
    'UPLOADED_FILES_USE_URL': False,
}





# import environment specific configuration
try:
    from pinpict.local_settings import *
except ImportError:
    print('settings importation error')
    pass




# set jwt token settings here because secret key (in local_settings) must be available
JWT_AUTH = {
    'JWT_ENCODE_HANDLER':
    'rest_framework_jwt.utils.jwt_encode_handler',

    'JWT_DECODE_HANDLER':
    'rest_framework_jwt.utils.jwt_decode_handler',

    'JWT_PAYLOAD_HANDLER':
    'rest_framework_jwt.utils.jwt_payload_handler',

    'JWT_PAYLOAD_GET_USER_ID_HANDLER':
    'rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler',

    'JWT_RESPONSE_PAYLOAD_HANDLER':
    'rest_framework_jwt.utils.jwt_response_payload_handler',

    'JWT_SECRET_KEY': SECRET_KEY,
    'JWT_ALGORITHM': 'HS256',
    'JWT_VERIFY': True,
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_LEEWAY': 0,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),
    'JWT_AUDIENCE': None,
    'JWT_ISSUER': None,

    'JWT_ALLOW_REFRESH': True,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=365),

    'JWT_AUTH_HEADER_PREFIX': 'JWT',
}
