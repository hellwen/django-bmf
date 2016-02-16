#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from djangobmf.models import Notification

from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import SerializerMethodField
from rest_framework.reverse import reverse


class NotificationViewSerializer(ModelSerializer):
    has_new_entry = SerializerMethodField()
    has_comments = SerializerMethodField()
    has_files = SerializerMethodField()
    has_detectchanges = SerializerMethodField()
    has_workflow = SerializerMethodField()
    enabled = SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            'new_entry',
            'comments',
            'files',
            'detectchanges',
            'workflow',
            'has_new_entry',
            'has_comments',
            'has_files',
            'has_detectchanges',
            'has_workflow',
            'enabled',
        ]

    def validate(self, data):
        """
        Check that the start is before the stop.
        """
        model = self.context['view'].get_bmfmodel()

        if "new_entry" in data and self.context['view'].kwargs.get('pk', None):
            data["new_entry"] = False

        if "comments" in data and not model._bmfmeta.has_comments:
            data["comments"] = False

        if "files" in data and not model._bmfmeta.has_files:
            data["files"] = False

        if "detectchanges" in data and not model._bmfmeta.has_detectchanges:
            data["detectchanges"] = False

        if "workflow" in data and not model._bmfmeta.has_workflow:
            data["workflow"] = False

        return data

    def get_has_new_entry(self, obj):
        return not bool(obj.watch_id)

    def get_has_comments(self, obj):
        return obj.watch_ct.model_class()._bmfmeta.has_comments

    def get_has_files(self, obj):
        return obj.watch_ct.model_class()._bmfmeta.has_files

    def get_has_detectchanges(self, obj):
        return obj.watch_ct.model_class()._bmfmeta.has_detectchanges

    def get_has_workflow(self, obj):
        return obj.watch_ct.model_class()._bmfmeta.has_workflow

    def get_enabled(self, obj):
        return self.get_has_workflow(obj) or self.get_has_detectchanges(obj) or \
            self.get_has_files(obj) or self.get_has_comments(obj)

    def create(self, validated_data):
        return Notification.objects.create(
            user=self.context['request'].user,
            watch_id=self.context['view'].kwargs.get('pk', None),
            watch_ct=self.context['view'].get_bmfcontenttype(),
            unread=False,
            **validated_data
        )


class NotificationListSerializer(NotificationViewSerializer):
    api = SerializerMethodField()
    name = SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            'name',
            'modified',
            'watch_id',
            'unread',
            'api',
            'new_entry',
            'comments',
            'files',
            'detectchanges',
            'workflow',
            'has_new_entry',
            'has_comments',
            'has_files',
            'has_detectchanges',
            'has_workflow',
            'enabled',
        ]

    def get_name(self, obj):
        return '%s' % obj.watch_object

    def get_api(self, obj):
        return reverse('djangobmf:api-notification', kwargs={
            'app': obj.watch_object._meta.app_label,
            'model': obj.watch_object._meta.model_name,
            'pk': obj.watch_id,
        })
