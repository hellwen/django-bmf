#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from djangobmf.serializers import ModuleSerializer


class EmployeeSerializer(ModuleSerializer):
    class Meta:
        fields = ['id', 'name', 'bmfdetail']
