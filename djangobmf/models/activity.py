#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from djangobmf.conf import settings as bmfsettings

import json


ACTION_COMMENT = 1
ACTION_CREATED = 2
ACTION_UPDATED = 3
ACTION_WORKFLOW = 4
ACTION_FILE = 5

ACTION_TYPES = (
    (ACTION_COMMENT, _("Comment")),
    (ACTION_CREATED, _("Created")),
    (ACTION_UPDATED, _("Updated")),
    (ACTION_WORKFLOW, _("Workflow")),
    (ACTION_FILE, _("File")),
)


class ActivityQuerySet(models.QuerySet):
    def comments(self):
        return self.filter(action=ACTION_COMMENT)


class ActivityManager(models.Manager):
    use_for_related_fields = True

    def get_queryset(self):
        return ActivityQuerySet(self.model, using=self._db)

    def comments(self):
        return self.get_queryset().comments()


@python_2_unicode_compatible
class Activity(models.Model):
    """
    Model which is accessed by en BMFModel with history
    """

    user = models.ForeignKey(
        getattr(settings, 'AUTH_USER_MODEL', 'auth.User'),
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    topic = models.CharField(_("Topic"), max_length=100, blank=True, null=True,)
    text = models.TextField(_("Text"), blank=True, null=True,)
    action = models.PositiveSmallIntegerField(
        _("Action"),
        blank=False,
        null=True,
        editable=False,
        default=ACTION_COMMENT,
        choices=ACTION_TYPES,
    )
    template = models.CharField(_("Template"), max_length=100, editable=False, blank=False, null=True)
    parent_id = models.PositiveIntegerField()
    parent_ct = models.ForeignKey(
        ContentType, related_name="bmf_history_parent", on_delete=models.CASCADE,
    )
    parent_object = GenericForeignKey('parent_ct', 'parent_id')

    modified = models.DateTimeField(_("Modified"), auto_now=True, editable=False,)

    objects = ActivityManager()

    class Meta:
        ordering = ('-modified',)
        verbose_name = _('Activity')
        verbose_name_plural = _('Activity')
        get_latest_by = "modified"
        abstract = True

    def __str__(self):
        if self.topic:
            return self.topic
        else:
            return '%s %s' % (self.user, self.pk)

    def get_symbol(self):
        if self.action == ACTION_WORKFLOW:
            return bmfsettings.ACTIVITY_WORKFLOW
        elif self.action == ACTION_COMMENT:
            return bmfsettings.ACTIVITY_COMMENT
        elif self.action == ACTION_UPDATED:
            return bmfsettings.ACTIVITY_UPDATED
        elif self.action == ACTION_FILE:
            return bmfsettings.ACTIVITY_FILE
        elif self.action == ACTION_CREATED:
            return bmfsettings.ACTIVITY_CREATED
        return bmfsettings.ACTIVITY_UNKNOWN

    def get_template(self):
        if self.template:
            return self.template
        if self.action == ACTION_WORKFLOW:
            return "djangobmf/activities/workflow.html"
        elif self.action == ACTION_FILE:
            return "djangobmf/activities/file.html"
        elif self.action == ACTION_UPDATED:
            return "djangobmf/activities/updated.html"
        elif self.action == ACTION_CREATED:
            return "djangobmf/activities/created.html"
        return "djangobmf/activities/message.html"

    def get_text(self):
        if self.action == ACTION_WORKFLOW:
            data = json.loads(self.text)
            return {
                'new': self.parent_object._bmfmeta.workflow.states[data['new']],
                'old': self.parent_object._bmfmeta.workflow.states[data['old']],
            }
        elif self.action == ACTION_FILE:
            data = json.loads(self.text)
            return data
        return self.text

    def get_json(self):
        return ''

    def changes(self):
        if self.action == ACTION_UPDATED:
            data = json.loads(self.text)
            # update field names with the fields verbose name (and therefore its translation)
            for i in range(len(data)):
                for field in self.parent_ct.model_class()._meta.fields:
                    if field.name == data[i][0]:
                        data[i][0] = field.verbose_name
                        break
            return data
        return self.text
