#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from djangobmf.models import BMFModel
from djangobmf.conf import settings

from .serializers import TeamSerializer


@python_2_unicode_compatible
class AbstractTeam(BMFModel):
    """
    """
    name = models.CharField(
        max_length=255, null=False, blank=False, editable=True,
    )
    members = models.ManyToManyField(
        settings.CONTRIB_EMPLOYEE, blank=True, related_name="teams",
        limit_choices_to={'user__isnull': False}, through='TeamMember',
    )

    class Meta(BMFModel.Meta):  # only needed for abstract models
        verbose_name = _('Team')
        verbose_name_plural = _('Teams')
        ordering = ['name']
        abstract = True
        swappable = "BMF_CONTRIB_TEAM"

    class BMFMeta:
        search_fields = ['name']
        has_logging = False
        serializer = TeamSerializer

    def __str__(self):
        return self.name


class TeamMember(BMFModel):
    team = models.ForeignKey(
        settings.CONTRIB_TEAM, null=True, blank=True, related_name="+", on_delete=models.CASCADE,
    )
    employee = models.ForeignKey(
        settings.CONTRIB_EMPLOYEE, null=True, blank=True, related_name="+", on_delete=models.CASCADE,
    )
    is_manager = models.BooleanField(_("Is manager"), default=False)

    class Meta:
        unique_together = ("team", "employee")

    class BMFMeta:
        only_related = True


class Team(AbstractTeam):
    pass
