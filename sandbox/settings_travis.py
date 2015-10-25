from sandbox.settings_common import *

# Common settings for testing

import tempfile

BMF_DOCUMENT_ROOT = tempfile.mkdtemp(prefix='djangobmf_')
BMF_DOCUMENT_URL = '/documents/'

CELERY_ALWAYS_EAGER=True # deactivate celery

INSTALLED_APPS += (
    'djangobmf',
#   'celery',
)

# The 'sqlite3' backend requires only the ENGINE setting (an in-
# memory database will be used). All other backends will require a
# NAME and potentially authentication information. See the
# following section in the docs for more information:
#
# https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/unit-tests/

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
#       'ENGINE': 'django.db.backends.postgresql_psycopg2',
#       'NAME': 'djangobmf',
#       'USER': 'postgres',
#       'HOST': '',
#       'PORT': '',
    }
}

try:
    from settings_local import *
except:
    pass
