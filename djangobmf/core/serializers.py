#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from djangobmf.models import Activity
from djangobmf.templatetags.djangobmf_markup import markdown_filter

from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import SerializerMethodField

import json

class ActivitySerializer(ModelSerializer):
    text = SerializerMethodField()
    user = SerializerMethodField()

    class Meta:
        model = Activity
        fields = ['user', 'topic', 'text', 'modified']

    def get_text(self, obj):
        return markdown_filter(obj.text)

    def get_user(self, obj):
        if hasattr(obj.user, 'get_full_name'):
            return obj.user.get_full_name()
        return '%s' % obj.user
