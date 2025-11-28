from pathlib import Path

import os
from dotenv import load_dotenv
IS_RENDER = os.getenv("RENDER", False)

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = ('(+$dka)c&)3^rz8xo*4z6!(wo7d1py=(ekc7=s!kng5ctv2dpg')

DEBUG = True


ALLOWED_HOSTS = ["paycollection.onrender.com", "localhost","127.0.0.1"]


CORS_ALLOWED_ORIGINS = [
    
    "http://localhost:5174",
    "https://neo.tecnavis.in",
    "https://paycollection-2h8k.onrender.com/"
]


INSTALLED_APPS = [
    'corsheaders', 
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    "main",
    "users",
    'financials',
    'customer',
    'collectionplans',
    
    
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', 
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'collection_management.urls'
CORS_ALLOW_ALL_ORIGINS = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'collection_management.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'thoufeeq_cash_collection',
        'USER': 'thoufeeq_cash_collection_user',
        'PASSWORD': 'HXJk7DJiEQHRIi67TRgIhPJm5fwkMZ8V',
        'HOST': 'dpg-d4kj3rre5dus73f8v6jg-a.oregon-postgres.render.com',
        'PORT': '5432',
        'OPTIONS': {
            'sslmode': 'require',
        },
    }
}




    #      {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': 'paycollection_db',
    #     'USER': 'postgres',
    #     'PASSWORD': 'Rashinechikunnu99@kt',
    #     'HOST': 'localhost',
    #     'PORT': '5432',
    # 








# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOWED_ORIGINS = [
    
    "http://localhost:5174",
    "https://neo.tecnavis.in"

]

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'


TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

from datetime import timedelta

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',  
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=3),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True, 
    "BLACKLIST_AFTER_ROTATION": True,  
    "UPDATE_LAST_LOGIN": True, 
    "AUTH_HEADER_TYPES": ("Bearer",),  
}

AUTH_USER_MODEL = 'users.CustomUser'

