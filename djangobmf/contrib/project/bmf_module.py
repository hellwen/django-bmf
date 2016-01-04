#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.dashboards import ProjectManagement
from djangobmf.sites import Module
from djangobmf.sites import ViewMixin
from djangobmf.sites import register

from .categories import ProjectCategory
from .models import Project
from .permissions import ProjectPermission
from .views import ProjectUpdateView


@register
class ProjectModule(Module):
    model = Project
    default = True
    update = ProjectUpdateView
    permissions = ProjectPermission


@register(category=ProjectCategory)
class ActiveProjects(ViewMixin):
    model = Project
    name = _("Active projects")
    slug = "active"

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(is_active=True)


@register(category=ProjectCategory)
class AllProjects(ViewMixin):
    model = Project
    name = _("All projects")
    slug = "all"
