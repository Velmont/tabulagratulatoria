import os

from .base import *


SECRET_KEY = get_env_setting('SECRET_KEY')

STATIC_ROOT = os.path.join(REPO_DIR, 'collected_staticfiles')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(REPO_DIR, 'db', 'db.sqlite3'),
    }
}

SERVER_EMAIL = 'Tabula gratulatoria <noreply@tg.s0.no>'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
DEFAULT_FROM_EMAIL = SERVER_EMAIL
EMAIL_SUBJECT_PREFIX = '[TG] '
