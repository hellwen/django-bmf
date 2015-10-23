#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

"""
overwrites bmf settings from django's settings
"""

# TODO OLD FILE REMOVE ME

from django.conf import settings
from django.core.files.storage import get_storage_class  # TODO OLD

# === storage =================================================================

bmf_storage = getattr(settings, 'BMF_STORAGE', {})
CFG_STORAGE = {
    'ENGINE': 'django.core.files.storage.FileSystemStorage',
    'OPTIONS': {},
    'SERVER': 'djangobmf.backends.DefaultServer',
    'STATIC_PREFIX': 'static',
}
CFG_STORAGE.update(bmf_storage)

if 'location' not in CFG_STORAGE['OPTIONS']:
    CFG_STORAGE['OPTIONS']['location'] = getattr(settings, 'BMF_DOCUMENT_ROOT', None)
if 'base_url' not in CFG_STORAGE['OPTIONS']:
    CFG_STORAGE['OPTIONS']['base_url'] = getattr(settings, 'BMF_DOCUMENT_URL', None)

if not CFG_STORAGE['OPTIONS']['location']:
    raise RuntimeError("django BMF module needs a setting BMF_DOCUMENT_ROOT")
if not CFG_STORAGE['OPTIONS']['base_url']:
    raise RuntimeError("django BMF module needs a setting BMF_DOCUMENT_URL")

DOCUMENT_ROOT = CFG_STORAGE['OPTIONS']['location']
DOCUMENT_URL = CFG_STORAGE['OPTIONS']['base_url']

STORAGE = get_storage_class(CFG_STORAGE['ENGINE'])
STORAGE_OPTIONS = CFG_STORAGE['OPTIONS']
STORAGE_STATIC_PREFIX = CFG_STORAGE['STATIC_PREFIX']
