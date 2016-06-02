#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.timesince import timesince
from django.utils.timezone import now

from djangobmf.serializers import ModuleSerializer

from rest_framework import serializers


class TimesheetSerializer(ModuleSerializer):
    time = serializers.SerializerMethodField()
    timesince = serializers.SerializerMethodField()
    employee_name = serializers.ReadOnlyField(source='employee.name')
    project_name = serializers.ReadOnlyField(source='project.name')

    class Meta:
        fields = (
            'time',
            'timesince',
            'summary',
            'start',
            'end',
            'billable',
            'valid',
            'employee',
            'employee_name',
            'project',
            'project_name',
            'task',
        )

    def get_time(self, obj):
        if obj.end:
            delta = obj.end - obj.start
        else:
            delta = now() - obj.start
        return delta.total_seconds()

    def get_timesince(self, obj):
        return timesince(obj.start, obj.end)
