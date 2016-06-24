#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from djangobmf.serializers import ModuleSerializer

from rest_framework import serializers


class WarehouseSerializer(ModuleSerializer):

    class Meta:
        fields = (
            'name',
        )


class LocationSerializer(ModuleSerializer):
    warehouse_name = serializers.ReadOnlyField(source='warehouse.name')

    class Meta:
        fields = (
            'name',
            'warehouse_name',
        )
