#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from djangobmf.models import Activity
from djangobmf.models import Notification
from djangobmf.models.activity import ACTION_COMMENT
from djangobmf.models.activity import ACTION_UPDATED
from djangobmf.models.activity import ACTION_CREATED
from djangobmf.models.activity import ACTION_WORKFLOW
from djangobmf.models.activity import ACTION_FILE
from djangobmf.signals import activity_comment
from djangobmf.templatetags.djangobmf_markup import markdown_filter

from rest_framework.serializers import ValidationError
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import SerializerMethodField

import json

class ActivitySerializer(ModelSerializer):
    user = SerializerMethodField()
    formatted = SerializerMethodField()
    json = SerializerMethodField()
    action = SerializerMethodField()

    class Meta:
        model = Activity
        fields = ['user', 'topic', 'text', 'formatted', 'json', 'action', 'modified']

    def validate(self, data):
        """
        Check that the start is before the stop.
        """
        if "topic" not in data:
            data["topic"] = ""
        if "text" not in data:
            data["text"] = ""
        if not data['topic'] and not data['text']:
            raise ValidationError(_("You need to define a topic or a text"))
        return data

    def create(self, validated_data):
        obj = Activity.objects.create(
            user=self.context['request'].user,
            action=ACTION_COMMENT,
            parent_id=self.context['view'].kwargs.get('pk'),
            parent_ct=self.context['view'].get_bmfcontenttype(),
            **validated_data
        )
        obj.save()
        obj.parent_object.modified = now()
        obj.parent_object.modified_by = self.context['request'].user
        obj.parent_object.save()
        activity_comment.send(sender=obj.__class__, instance=obj)
        return obj

    def get_user(self, obj):
        if hasattr(obj.user, 'get_full_name'):
            return obj.user.get_full_name()
        return '%s' % obj.user

    def get_formatted(self, obj):
        if obj.action in [ACTION_COMMENT]:
            return markdown_filter(obj.text)
        return None

    def get_json(self, obj):
        if obj.action in [ACTION_WORKFLOW, ACTION_UPDATED]:
            return json.loads(obj.text)
        return None

    def get_action(self, obj):
        if obj.action == ACTION_CREATED:
            return 'created'
        if obj.action == ACTION_WORKFLOW:
            return 'workflow'
        if obj.action == ACTION_UPDATED:
            return 'updated'
        if obj.action == ACTION_COMMENT:
            return 'comment'
        return None


class NotificationSerializer(ModelSerializer):
    has_new_entry = SerializerMethodField()
    has_comments = SerializerMethodField()
    has_files = SerializerMethodField()
    has_detectchanges = SerializerMethodField()
    has_workflow = SerializerMethodField()

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

    def create(self, validated_data):
        return Notification.objects.create(
            user=self.context['request'].user,
            watch_id=self.context['view'].kwargs.get('pk', None),
            watch_ct=self.context['view'].get_bmfcontenttype(),
            unread=False,
            **validated_data
        )
