#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.categories import ProjectManagement
from djangobmf.sites import Category


class ProjectCategory(Category):
    class Meta:
        name = _('Projects')
        slug = "projects"
        dashboard = ProjectManagement
