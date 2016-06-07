#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from djangobmf.serializers import ModuleSerializer
from rest_framework import serializers


class EmployeeSerializer(ModuleSerializer):
    user_name = serializers.ReadOnlyField(source='user.username')
    product_name = serializers.ReadOnlyField(source='product.name')

    class Meta:
        fields = ('name', 
            'user',
            'user_name', 
            'product',
            'product_name',
            'email',
            'phone_office',
            'phone_mobile',
        )
