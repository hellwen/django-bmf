#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now

from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class Notification(models.Model):
    """
    Model which informs users about changes in the history
    """
    user = models.ForeignKey(
        getattr(settings, 'AUTH_USER_MODEL', 'auth.User'), blank=True,
        null=True, on_delete=models.CASCADE,
    )

    watch_ct = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    watch_id = models.PositiveIntegerField(null=True, db_index=True)
    watch_object = GenericForeignKey('watch_ct', 'watch_id')

    triggered = models.BooleanField(_("Triggered"), default=True, editable=False, db_index=True)
    unread = models.BooleanField(_("Unread"), default=True, editable=False, db_index=True)
    last_seen_object = models.PositiveIntegerField(null=True)

    new_entry = models.BooleanField(_("New entry"), default=False, db_index=True)
    comments = models.BooleanField(_("Comment written"), default=False, db_index=True)
    files = models.BooleanField(_("File added"), default=False, db_index=True)
    detectchanges = models.BooleanField(_("Object changed"), default=False, db_index=True)
    workflow = models.BooleanField(_("Workflowstate changed"), default=False, db_index=True)

    modified = models.DateTimeField(_("Modified"), editable=False, null=True, default=now)

    class Meta:
        unique_together = (('user', 'watch_ct', 'watch_id'),)
        ordering = ('-modified',)
        verbose_name = _('Watched activity')
        verbose_name_plural = _('Watched activities')
        get_latest_by = "modified"
        default_permissions = ()
        abstract = True

    def is_active(self):
        return self.comments or self.files or self.detectchanges or self.workflow

    def __str__(self):
        return '%s %s %s' % (self.user, self.watch_ct, self.watch_id)
