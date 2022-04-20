"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 3.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-c6t0j1ps%x=5%1nuggr7(#1j62uc$56aju2u_fgb5f_y4=*224'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #
    "graphene_django",
    'rest_framework',
    'rest_framework.authtoken',
    'graphql_jwt.refresh_token.apps.RefreshTokenConfig',
    # "graphql_auth",
    'drf_yasg',
    'djoser',
    'django_filters',
    'corsheaders',
    #
    "apps.account.apps.AccountsConfig",
    "apps.clients.apps.ClientsConfig",
    "apps.dash.apps.DashConfig",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'
AUTH_USER_MODEL = "account.Users"
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ["templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': "d39og1aadlht5s",
        'USER': "mluijfgijaivkx",
        'PASSWORD': "9d36ff51c5c6a2804ed86324fa4260cb0cefc0993a79907f5877217c00ee2d27",
        'HOST': "ec2-52-73-155-171.compute-1.amazonaws.com",
        'PORT': "5432",  # 5432 by default
    },

    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': os.getenv('TTM_DATA_BASE_NAME'),
#         'USER': os.getenv('TTM_USER_NAME'),
#         'PASSWORD': os.getenv('TTM_PASSEWORD'),
#         'HOST': 'localhost',
#         'PORT': '3306',
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/


LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/


#
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
#

# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, 'staticfiles'),
# )

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CORS_ALLOW_ALL_ORIGINS = True
REST_FRAMEWORK = {
    "SEARCH_PARAM": "q",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication'
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        'rest_framework.permissions.AllowAny',
    ],
    "DEFAULT_PAGINATION_CLASS": 'rest_framework.pagination.LimitOffsetPagination',
    "PAGE_SIZE": 100,

}

DJOSER = {
    'SEND_ACTIVATION_EMAIL': False,
    'SERIALIZERS': {},
}

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    # "graphql_auth.backends.GraphQLAuthBackend",
]

GRAPHQL_AUTH = {
    'LOGIN_ALLOWED_FIELDS': ['phone', 'email'],
    'REGISTER_MUTATION_FIELDS': ['phone', 'email'],
    'UPDATE_MUTATION_FIELDS': [],
    'USER_NODE_EXCLUDE_FIELDS': ["password"]
}

GRAPHQL_JWT = {
    'JWT_VERIFY_EXPIRATION': False,
    'JWT_LONG_RUNNING_REFRESH_TOKEN': True,
    # 'JWT_AUTH_HEADER_PREFIX' : "IAGP_TOKEN"
}

GRAPHENE = {
    "ATOMIC_MUTATIONS": True,
    "SUBSCRIPTION_PATH": "/ws/graphql",
    "DJANGO_CHOICE_FIELD_ENUM_V3_NAMING": True,
    # 'SCHEMA': 'config.schema.schema',  # this file doesn't exist yet
    'MIDDLEWARE': [
        'graphql_jwt.middleware.JSONWebTokenMiddleware',
    ],
}
