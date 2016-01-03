#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
# from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class NumberRange(models.Model):
    ct = models.ForeignKey(
        ContentType,
        related_name="+",
        null=True,
        blank=False,
        editable=False,
    )
    period_start = models.DateField(null=True, blank=False, db_index=True)
    period_final = models.DateField(null=True, blank=False, db_index=True)
    counter = models.PositiveIntegerField(null=True, blank=False, default=1)

    class Meta:
        abstract = True
        unique_together = (('ct', 'period_start', 'period_final')),

    def __str__(self):
        return 'NumberRange %s' % self.ct_id
