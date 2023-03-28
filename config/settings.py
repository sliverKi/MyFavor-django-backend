from decouple import config
from pathlib import Path
import os
import environ
import my_settings
import dj_database_url

env = environ.Env()

BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

SECRET_KEY = env("SECRET_KEY")

ALLOWED_HOSTS = ["*"]
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
]

CUSTOM_APPS = [
    "users.apps.UsersConfig",
    "usersCalendar.apps.UserscalendarConfig",
    "common.apps.CommonConfig",
    "media.apps.MediaConfig",
    "idols.apps.IdolsConfig",
    "categories.apps.CategoriesConfig",
]

SYSTEM_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
INSTALLED_APPS = SYSTEM_APPS + THIRD_PARTY_APPS + CUSTOM_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DEBUG = 'RENDER' not in os.environ


DATABASES =env("DATABASES")

STATIC_URL = '/static/'
if not DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "ko-kr"

TIME_ZONE = "Asia/Seoul"

DATE_INPUT_FORMATS = ["%Y-%m-%d"]

DATE_FORMAT = "F j"

USE_I18N = False

USE_TZ = False

STATIC_URL = "/static/"
if not DEBUG:
    STATIC_ROOT=os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_STORAGE="whitenoise.storage.CompressedManifestStaticFilesStorage"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "users.User"

MEDIA_ROOT = "uploads"

MEDIA_URL = "user-uploads/"

CORS_ALLOW_CREDENTIALS = True

CORS_ORIGIN_ALLOW = True
CORS_ALLOWED_ORIGINS_ALL = True
CSRF_TRUSTED_ORIGINS = ["http://*.myfavor.co.kr", "https://*.myfavor.co.kr"]


CF_TOKEN=env("CF_TOKEN")
CF_ID=env("CF_ID")

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ]
}

ACCOUNT_PASSWORD_INPUT_RENDER_VALUE = True  
ACCOUNT_SESSION_REMEMBER = True  
SESSION_COOKIE_AGE = 3600
SESSION_EXPIRE_AT_BROWSER_CLOSE = False