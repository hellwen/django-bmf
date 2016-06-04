#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from djangobmf.serializers import ModuleSerializer

from rest_framework import serializers


class QuotationSerializer(ModuleSerializer):
    state_name = serializers.ReadOnlyField(source='state.name')
    project_name = serializers.ReadOnlyField(source='project.name')

    net = serializers.SerializerMethodField()
    gross = serializers.SerializerMethodField()
    taxes = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'quotation_number',
            'state',
            'state_name',
            'project',
            'project_name',
            'net',
            'gross',
            'taxes',
            'completed',
        )

    def get_net(self, obj):
        return obj.calc_net()

    def get_gross(self, obj):
        return obj.calc_gross()

    def get_taxes(self, obj):
        return [{'name': t[0].name, 'value': t[1]} for t in obj.calc_taxes()]

class QuotationProductSerializer(ModuleSerializer):
    unitprice = serializers.SerializerMethodField()
    net = serializers.SerializerMethodField()
    gross = serializers.SerializerMethodField()
    taxes = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'name',
            'description',
            'unitprice',
            'price',
            'amount',
            'net',
            'gross',
            'taxes',
        )

    def get_unitprice(self, obj):
        return obj.calc_net_unit()

    def get_net(self, obj):
        return obj.calc_net()

    def get_gross(self, obj):
        return obj.calc_gross()

    def get_taxes(self, obj):
        return [{'name': t[0].name, 'value': t[1]} for t in obj.calc_taxes()]
