#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.dashboards import ProjectManagement
from djangobmf.sites import Category


class GoalCategory(Category):
    name = _('Goals')
    slug = "goals"
    dashboard = ProjectManagement


class TaskCategory(Category):
    name = _('Tasks')
    slug = "tasks"
    dashboard = ProjectManagement
