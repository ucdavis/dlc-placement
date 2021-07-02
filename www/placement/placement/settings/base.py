"""
Django settings for placement project.

Generated by 'django-admin startproject' using Django 1.9.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
if(os.environ['DEBUG_APP'] == 'True'):
  DEBUG = True

ALLOWED_HOSTS = []


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
# Third party apps    
    'crispy_forms',
# CAS apps
    'django_cas_ng',
# CSV apps
    'djqscsv',    
# Custom apps
    'languages',
    'levels',
    'scoresheet',
    'home',
    'users',
    'languages_users'
]

#Crispy form templates for bootstrap
CRISPY_TEMPLATE_PACK = 'bootstrap3'

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Added for CAS Authentication
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'django_cas_ng.backends.CASBackend',
)

# Added for CAS configuration
# testing server
CAS_SERVER_URL = os.environ['CAS_SERVER_URL']

# Create a user when the CAS authentication is successful.
CAS_CREATE_USER = False

# logging out of the application, log the user out of CAS as well.
CAS_LOGOUT_COMPLETELY = True

CAS_IGNORE_REFERER=True

#Where to send a user after logging in or out if there is no referrer and no next page set.
CAS_REDIRECT_URL = '/users/validate/'

#an unknown or invalid ticket is received, the user is redirected back to the login page.
CAS_RETRY_LOGIN=True

ROOT_URLCONF = 'placement.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates"),
                  os.path.join(BASE_DIR, "templates/languages"),
                  os.path.join(BASE_DIR, "templates/levels"),
                  os.path.join(BASE_DIR, "templates/scoresheets"),
                  os.path.join(BASE_DIR, "templates/home"),
                  os.path.join(BASE_DIR, "templates/users"),
                  os.path.join(BASE_DIR, "templates/languages_users"),
                  os.path.join(BASE_DIR, "templates/email"),
                 ],
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

WSGI_APPLICATION = 'placement.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': os.path.join(BASE_DIR, 'db/db.sqlite3'), # can become dlc_users
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dlc_django_data',
        'USER': 'root',
        'PASSWORD': 'mysql_passwd',
        'HOST': 'docker.for.mac.localhost',
        'PORT': '3306',
    },
    'production': {
        #'ENGINE': 'django.db.backends.sqlite3', # can become dlc_data
        #'NAME':os.path.join(BASE_DIR, 'db/production.sqlite3'),
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dlc_data',
        'USER': 'root',
        'PASSWORD': 'mysql_passwd',
        'HOST': 'docker.for.mac.localhost',
        'PORT': '3306',
    }, 
}

DATABASE_ROUTERS = ['levels.router.LevelsRouter',
                    'languages.router.LanguageRouter',
                    'scoresheet.router.ScoresheetRouter',
                    'users.router.UsersRouter',
                    'languages_users.router.LanguagesUsersRouter',
                    ]

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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

EMAIL_HOST = os.environ['EMAIL_HOST']
EMAIL_PORT = os.environ['EMAIL_PORT']
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_USE_TLS = os.environ['EMAIL_USE_TLS']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
EMAIL_FROM = os.environ['EMAIL_FROM']

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_URL = '/static/'
STATICFILES_DIRS = [
                    os.path.join(BASE_DIR, "static"),
                    ]
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR),"static_cdn")

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '[contactor] %(levelname)s %(asctime)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'WARN',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'WARN',
            'propagate': False,
        },
    }
}
