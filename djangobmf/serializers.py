#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from djangobmf import fields
from rest_framework import serializers
from rest_framework.fields import CharField
from rest_framework.fields import DecimalField


class ModuleSerializer(serializers.ModelSerializer):

    bmfdetail = serializers.SerializerMethodField()

    # TODO apply different serializer to only_related models
    def get_bmfdetail(self, obj):
        if obj._bmfmeta.only_related:
            return '#'

        return obj.bmfmodule_detail()


class MoneyField(DecimalField):
    def to_representation(self, value):
        return value.value
ModuleSerializer.serializer_field_mapping[fields.MoneyField] = MoneyField


class WorkflowField(CharField):
    def to_representation(self, value):
        return value.key
ModuleSerializer.serializer_field_mapping[fields.WorkflowField] = WorkflowField


# class DocumentSerializer(serializers.HyperlinkedModelSerializer):
#   class Meta:
#       model = apps.get_model('djangobmf', 'Document')
#       fields = ['pk']
