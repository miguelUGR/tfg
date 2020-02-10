"""
Django settings for aplicacion project.

Generated by 'django-admin startproject' using Django 2.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'zjfv$ys!&--!wds!$#2ub*yb0yhvc+ke9eic^1jtq=0sf!r$k0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

#ALLOWED_HOSTS = []
ALLOWED_HOSTS = ['*'] #añadimos '*' para que arranque desde cualquier lado


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.sites', # new p6
    'allauth', # new p6
    'allauth.account', # new p6 AÑADE Email Addresses login.html (account_signup...etc) son las direcciones propias de DJANGO
    'allauth.socialaccount', # new p6s

    'desarrollo', #nuevo
    'django_cleanup.apps.CleanupConfig' # PARA ELIMINACION AUTOMATICA imagen de Observaciones
]
SITE_ID = 1 #IMPORTANTISsIMO TENERLO PARA ENTRAR EN /admin
AUTH_USER_MODEL = 'desarrollo.Usuario' #Esto es para poder coger el modelo usuario creado a partir del propio de django
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'aplicacion.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')], #nuevo
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

#------------------------P6----------------------------------
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)
LOGIN_REDIRECT_URL = "base" # esto es en caso de que haga el login correctamente te manda donde digas
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' #para que no pete cuando metes un correo, pk ten manda un correo de autentificacion en modo pro cuando metes un correo

ACCOUNT_EMAIL_REQUIRED = True #para que cuando me registre no sea opcional
ACCOUNT_FORMS ={ 'signup':'desarrollo.forms.MiSignupForm',} #para que coja la clase y añada los campos que queremos para registrarse desde la web
# LOGIN_URL = '/account/login/'
#-------------------------------------------------------------

#----Carpeta para la imagen (ImageField)------------------------
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
#-------------------------------------------------------------


WSGI_APPLICATION = 'aplicacion.wsgi.application'


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

#------------------------------------COMENTAMOS LO SIGUIENTE-----------------------------
# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

#LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')] #busque los archivos en static
