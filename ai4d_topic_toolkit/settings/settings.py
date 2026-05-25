"""
Django settings for ai4d_topic_toolkit project.

Defaults are tuned for local development (SQLite, DEBUG=True). Production
deployments should use ai4d_topic_toolkit.settings.staging.
"""
import os
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = config(
    'SECRET_KEY',
    default='django-insecure-toolkit-dev-only-do-not-use-in-prod-CHANGE-ME',
)

DEBUG = True

ALLOWED_HOSTS = ['*']

CORS_ALLOW_ALL_ORIGINS = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'topic_extraction',
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

ROOT_URLCONF = 'ai4d_topic_toolkit.urls'

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

WSGI_APPLICATION = 'ai4d_topic_toolkit.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# HuggingFace token — optional for local dev; required for first model download
# behind authenticated proxies. Empty default avoids forcing operators to set
# the env var for fully local runs once models are cached.
HUGGING_TOKEN = config('HUGGING_TOKEN', default='')

# Topic extraction settings — defaults match the empirically-validated
# production configuration (mpnet + per-article z-score normalization).
# The full 'embedding' extractor (zero-shot NLI) is available via
# EXTRACTION_BACKEND='embedding' if the slower signal is wanted.
EXTRACTION_BACKEND = config('EXTRACTION_BACKEND', default='embedding_similarity')
EMBEDDING_MODEL_NAME = config('EMBEDDING_MODEL_NAME', default='sentence-transformers/paraphrase-multilingual-mpnet-base-v2')
ZERO_SHOT_MODEL_NAME = config('ZERO_SHOT_MODEL_NAME', default='MoritzLaurer/mDeBERTa-v3-base-mnli-xnli')
LLM_MODEL_NAME = config('LLM_MODEL_NAME', default='Qwen/Qwen2.5-3B-Instruct')
EMBEDDING_THRESHOLD = float(config('EMBEDDING_THRESHOLD', default='0.35'))
EMBEDDING_Z_THRESHOLD = float(config('EMBEDDING_Z_THRESHOLD', default='1.0'))

# Topic extraction — language coverage
TOPIC_LANGUAGES = ['en', 'el', 'de']
DEFAULT_LANGUAGE = 'en'
LANG_DETECT_MIN_CHARS = 30

# Opengov ingestor — parquet location for backfill_embeddings.
# Default is BASE_DIR/resources/deliberations/opengov_deliberations_v2.parquet
# but the ingestor falls back to that path internally if OPENGOV_PARQUET_PATH
# isn't set. Setting it here documents the contract for operators.
OPENGOV_PARQUET_PATH = config(
    'OPENGOV_PARQUET_PATH',
    default=str(BASE_DIR / 'resources' / 'deliberations' / 'opengov_deliberations_v2.parquet'),
)
