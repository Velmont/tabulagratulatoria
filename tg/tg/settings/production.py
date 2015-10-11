import os

from .base import *


SECRET_KEY = get_env_setting('SECRET_KEY')

STATIC_ROOT = os.path.join(REPO_DIR, 'collected_staticfiles')
