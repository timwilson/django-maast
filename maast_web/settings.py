"""
Django settings for maast_web project.

Generated by 'django-admin startproject' using Django 5.0rc1.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

from decouple import config
from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=False, cast=bool)

if DEBUG:
    API_HOST = config("DEVELOPMENT_API_HOST")
    SITE_DOMAIN = config("DEVELOPMENT_SITE_DOMAIN")
else:
    API_HOST = config("PRODUCTION_API_HOST")
    SITE_DOMAIN = config("PRODUCTION_SITE_DOMAIN")

ALLOWED_HOSTS = []

INTERNAL_IPS = ["127.0.0.1"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    # Local
    "maast.apps.MaastConfig",
    "blog.apps.BlogConfig",
    "pages",
    # Third-party
    "tailwind",
    "theme",
    "django_browser_reload",
    "fontawesomefree",
    "meta",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

ROOT_URLCONF = "maast_web.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "maast/templates",
            BASE_DIR / "theme/templates",
            BASE_DIR / "blog/templates",
        ],
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

WSGI_APPLICATION = "maast_web.wsgi.application"


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "maast.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

# Default primary key field type
# https://docs.djangoproject.com/en/dev/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Custom configurations

# Tailwind CSS
TAILWIND_APP_NAME = "theme"

# django-meta settings
META_SITE_PROTOCOL = "https"
META_SITE_DOMAIN = "records.themnaa.org"
META_SITE_TYPE = "website"
META_SITE_NAME = "MAA Score Tabulator"
META_INCLUDE_KEYWORDS = [
    "archery",
    "minnesota archers alliance",
    "maa",
    "state records",
    "target archery",
    "nfaa",
    "national field archery association",
    "usa archery",
    "s3da",
    "scholastic 3d archery",
]
META_DEFAULT_KEYWORDS = [
    "archery",
    "minnesota archers alliance",
    "maa",
    "state records",
    "target archery",
    "nfaa",
    "national field archery association",
    "usa archery",
    "s3da",
    "scholastic 3d archery",
]
META_USE_OG_PROPERTIES = True
META_USE_TWITTER_PROPERTIES = False
META_USE_TITLE_TAG = True
META_DEFAULT_IMAGE = "/static/img/MAAST-og.png"
