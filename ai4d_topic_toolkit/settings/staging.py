from .settings import *
from decouple import config


DEBUG = False

SECRET_KEY = config('SECRET_KEY')

# Defense against accidentally inheriting the dev default. The dev default
# in settings.py ends in 'CHANGE-ME' as a self-documenting marker; if it
# somehow propagates through to staging, fail loudly at import time rather
# than silently boot with an insecure key.
if SECRET_KEY.endswith('CHANGE-ME') or 'django-insecure' in SECRET_KEY:
    raise RuntimeError(
        'staging.py loaded with a development SECRET_KEY. Set the SECRET_KEY '
        'environment variable to a production-grade value before deploying.'
    )

POSTGRES_USER = config('POSTGRES_USER')
POSTGRES_PASSWORD = config('POSTGRES_PASSWORD')
POSTGRES_PORT = config('POSTGRES_PORT', default='5432')
POSTGRES_DB = config('POSTGRES_DB', default='postgres')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': POSTGRES_DB,
        'USER': POSTGRES_USER,
        'PASSWORD': POSTGRES_PASSWORD,
        'HOST': 'db',
        'PORT': POSTGRES_PORT,
    }
}
