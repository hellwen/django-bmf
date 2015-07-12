#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.categories import ProjectManagement
from djangobmf.sites import Category


class GoalCategory(Category):
    class Meta:
        name = _('Goals')
        slug = "goals"
        dashboard = ProjectManagement


class TaskCategory(Category):
    class Meta:
        name = _('Tasks')
        slug = "tasks"
        dashboard = ProjectManagement
