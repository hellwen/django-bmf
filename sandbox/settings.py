from sandbox.settings_common import *

import os
import tempfile

# === DOCKER ------------------------------------------------------------------

if "DOCKER" in os.environ:
    INSTALLED_APPS += (
        'celery',
    )
    INSTALLED_APPS += TEST_PROJECT_APPS

    # BMF ==============================================================================

    BMF_DOCUMENT_ROOT = os.path.join(PROJECT_PATH, "documents")
    BMF_DOCUMENT_URL = '/documents/'

    # LOCAL SETTINGS ==================================================================

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'postgres',
            'USER': 'postgres',
            'HOST': 'postgres',
            'PORT': '5432',
        }
    }

    BROKER_URL = 'redis://redis:6379/0'
    CELERY_RESULT_BACKEND = 'redis://redis:6379/0'

# === TRAVIS ------------------------------------------------------------------

if "TRAVIS" in os.environ:
    BMF_DOCUMENT_ROOT = tempfile.mkdtemp(prefix='djangobmf_')
    BMF_DOCUMENT_URL = '/documents/'

    CELERY_ALWAYS_EAGER=True # deactivate celery

    INSTALLED_APPS += (
        'djangobmf',
    #   'celery',
    )

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
#           'ENGINE': 'django.db.backends.postgresql_psycopg2',
#           'NAME': 'djangobmf',
#           'USER': 'postgres',
#           'HOST': '',
#           'PORT': '',
        }
    }

# === OVERWRITE WITH LOCAL SETTINGS -------------------------------------------

try:
    from settings_local import *
except:
    pass
