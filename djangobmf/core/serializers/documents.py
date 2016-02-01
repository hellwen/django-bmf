#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from djangobmf.models import Document

from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import SerializerMethodField
from rest_framework.reverse import reverse


class DocumentsSerializer(ModelSerializer):
    download = SerializerMethodField()
    details = SerializerMethodField()

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        list_serializer = kwargs.pop('list', False)
        detail_serializer = kwargs.pop('list', False)

        super(DocumentsSerializer, self).__init__(*args, **kwargs)

        if list_serializer or detail_serializer:
            self.fields.pop('file')
            if list_serializer:
                self.fields.pop('description')
                self.fields.pop('sha1')
                self.fields.pop('is_static')
                self.fields.pop('modified')
                self.fields.pop('created')

    def get_download(self, obj):
        return reverse(
            'djangobmf:api-document-download',
            request=self.request,
            kwargs={'pk': obj.pk},
        )

    class Meta:
        model = Document
        fields = [
            'pk', 'name', 'mimetype', 'description', 'file',
            'size', 'sha1', 'is_static', 'modified',
            'created', 'download', 'details',
        ]
