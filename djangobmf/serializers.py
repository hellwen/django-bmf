from django.apps import apps
from djangobmf import fields
from rest_framework import serializers
from rest_framework.fields import CharField
from rest_framework.fields import DecimalField


class ModuleSerializer(serializers.ModelSerializer):

    bmfdetail = serializers.SerializerMethodField()

    def get_bmfdetail(self, obj):
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
