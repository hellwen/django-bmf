#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.core.files.storage import FileSystemStorage
from django.utils.functional import LazyObject
from django.utils.module_loading import import_string

from djangobmf.conf import settings


class Storage(FileSystemStorage):
    def __init__(self):

        assert settings.DOCUMENT_ROOT, "django BMF module needs a setting BMF_DOCUMENT_ROOT"
        assert settings.DOCUMENT_URL, "django BMF module needs a setting BMF_DOCUMENT_URL"

        super(Storage, self).__init__(
            location=settings.DOCUMENT_ROOT,
            base_url=settings.DOCUMENT_URL,
            file_permissions_mode=settings.DOCUMENT_PERMISSIONS_FILE,
            directory_permissions_mode=settings.DOCUMENT_PERMISSIONS_DIR,
        )

    def get_available_name(self, name):
        if name.startswith(settings.DOCUMENT_STATIC_PREFIX):
            if self.exists(name):
                self.delete(name)
            return name
        return super(Storage, self).get_available_name(name)


class DefaultStorage(LazyObject):
    def _setup(self):
        self._wrapped = import_string(settings.DOCUMENT_STORAGE)()


default_storage = DefaultStorage()
