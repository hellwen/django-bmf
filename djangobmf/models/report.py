#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# from django.http import HttpResponse

# from djangobmf.core.report import Report as BaseReport
# from djangobmf.models.renderer import Renderer


class Report(models.Model):
    """
    Model to store informations to generate a report
    """
    name = models.CharField(_('Name'), max_length=120)
    slug = models.CharField(_('Slug'), max_length=120)

    contenttype = models.ForeignKey(
        ContentType, related_name="bmf_report", null=True, blank=True,
        on_delete=models.CASCADE,
    )
    renderer_ct = models.ForeignKey(
        ContentType, related_name="+", null=True, blank=True,
        on_delete=models.CASCADE,
    )
    renderer_pk = models.PositiveIntegerField(null=True, blank=True)

    renderer_view = models.CharField(max_length=254)

    has_object = models.NullBooleanField()

    renderer = GenericForeignKey('renderer_ct', 'renderer_pk')

    enabled = models.BooleanField(default=False)

    modified = models.DateTimeField(_("Modified"), auto_now=True, null=True, editable=False)
    created = models.DateTimeField(_("Created"), auto_now_add=True, null=True, editable=False)

    class Meta:
        verbose_name = _('Report')
        verbose_name_plural = _('Reports')
        get_latest_by = "modified"
        unique_together = [["slug", "contenttype"]]
        abstract = True

    def __str__(self):
        return '%s' % self.slug
