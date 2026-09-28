import os
from pathlib import Path

from dotenv import load_dotenv


# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent


# Load environment variables from backend/.env
load_dotenv(BASE_DIR / ".env")


# Security
SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
    "dev-only-secret-key"
)

DEBUG = os.getenv(
    "DEBUG",
    "True"
).lower() == "true"

ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv(
        "ALLOWED_HOSTS",
        "127.0.0.1,localhost"
    ).split(",")
    if host.strip()
]


# Installed applications
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",
    "corsheaders",
    "api",
]


# Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# URLs / WSGI
ROOT_URLCONF = "assistant.urls"

WSGI_APPLICATION = "assistant.wsgi.application"


# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Internationalization
LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = True


# Static files
STATIC_URL = "static/"

STATIC_ROOT = BASE_DIR / "staticfiles"


# Uploaded files
MEDIA_ROOT = BASE_DIR / "media"

MEDIA_URL = "/media/"


# Default primary key
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# CORS
CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ALLOWED_ORIGINS",
        "http://localhost:5173"
    ).split(",")
    if origin.strip()
]


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.8-flash"
)

GEMINI_EMBEDDING_MODEL = os.getenv(
    "GEMINI_EMBEDDING_MODEL",
    "gemini-embedding-001"
)