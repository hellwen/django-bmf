#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.formats import date_format

from djangobmf.serializers import ModuleSerializer

from rest_framework import serializers


class StockSerializer(ModuleSerializer):
    class Meta:
        fields = (
            'bill_no',
        )

    def get_modified_date(self, obj):
        return date_format(obj.modified, "SHORT_DATE_FORMAT")


class StockProductSerializer(ModuleSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    location_name = serializers.ReadOnlyField(source='location.name')

    class Meta:
        fields = (
            'product_name',
            'price',
            'amount',
            'location_name',
        )
