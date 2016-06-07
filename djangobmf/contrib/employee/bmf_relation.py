#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.sites import register
from djangobmf.sites import Relationship

from .models import Employee


@register(model_from=Employee)
class TeamEmployeesRelationship(Relationship):
    name = _("Employees")
    slug = "employee"
    field = "members"
    model_to = "djangobmf_team.Team"
    settings = "BMF_CONTRIB_TEAM"
    template = "djangobmf_employee/employee_related_team.html"
