#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from djangobmf.serializers import ModuleSerializer

from rest_framework import serializers


class ProductSerializer(ModuleSerializer):
    class Meta:
        fields = (
            'name',
            'code',
            'type',
            'can_sold',
            'can_purchased',
            'price',
        )


class ProductTaxSerializer(ModuleSerializer):
    name = serializers.ReadOnlyField(source='tax.name')

    class Meta:
        fields = (
            'name',
            'tax',
            'included',
        )
