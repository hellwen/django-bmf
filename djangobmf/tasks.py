#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils import six

from djangobmf.decorators import optional_celery
from djangobmf.notification.tasks import djangobmf_user_watch

import hashlib


__all__ = [
    'djangobmf_user_watch',
    'generate_sha1',
]

if six.PY2:
    class FileNotFoundError(OSError):
        pass


@optional_celery
def generate_sha1(pk):
    from djangobmf.models import Document

    obj = Document.objects.get(pk=pk)

    hash = hashlib.sha1()

    try:
        obj.file.open('rb')
        if obj.file.multiple_chunks():
            for chunk in obj.file.chunks():
                hash.update(chunk)
        else:
            hash.update(obj.file.read())
        obj.file.close()
        Document.objects.filter(pk=pk).update(sha1=hash.hexdigest())

    except FileNotFoundError:
        pass
