import os
from decouple import config
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

#! SECURITY WARNING: keep the secret key used in production secret!
#! SECURITY WARNING: don't run with debug turned on in production!
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', cast=bool)

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'corsheaders',
    'rest_framework',
    'drf_yasg',

    # my apps
    'api.blog_api',
    'api.anidb_api',
    'apps.blog',
    'apps.anidb',
    'apps.oauth'
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

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates'],
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

WSGI_APPLICATION = 'core.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('POSTGRES_DB'),
        'USER': config('POSTGRES_USER'),
        'PASSWORD': config('POSTGRES_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Password validation
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static (CSS, JavaScript, Images)
STATIC_URL = '/static/'

# Media
MEDIA_URL = '/media/'
MEDIAR_ROOT = os.path.join(BASE_DIR, 'media')



# Permissions:
#   AllowAny
#   IsAuthenticated
#   IsAdminUser
#   IsAuthenticatedOrReadOnly

REST_FRAMEWORK = {
   'DEFAULT_PERMISSION_CLASSES': ( 
        'rest_framework.permissions.AllowAny', 
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
 
}


CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
]

# SECURE_REFERRER_POLICY = 'no-referrer-when-downgrade' 


# SOCIAL_AUTH_VK_OAUTH2_ID = config('SOCIAL_AUTH_VK_OAUTH2_KEY')
# SOCIAL_AUTH_VK_OAUTH2_SECRET = config('SOCIAL_AUTH_VK_OAUTH2_SECRET')


LOGIN_URL = 'auth/login/'