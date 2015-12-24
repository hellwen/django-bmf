#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from djangobmf.models import Activity

from rest_framework.serializers import ModelSerializer

class ActivitySerializer(ModelSerializer):
    class Meta:
        model = Activity
