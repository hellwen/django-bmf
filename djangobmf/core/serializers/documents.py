#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from djangobmf.models import Document

from rest_framework.serializers import ModelSerializer


class DocumentsSerializer(ModelSerializer):

    def __init__(self, *args, **kwargs):
        list_serializer = kwargs.pop('list', False)

        super(DocumentsSerializer, self).__init__(*args, **kwargs)

        if list_serializer:
            self.fields.pop('description')

    class Meta:
        model = Document
        fields = [
            'name', 'mimetype', 'description',
            'size', 'sha1', 'is_static', 'modified',
            'created',
        ]
