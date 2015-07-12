#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.categories import ViewFactory
from djangobmf.categories import ProjectManagement
from djangobmf.sites import site

from .categories import ProjectCategory
from .models import Project
from .permissions import ProjectPermission
from .serializers import ProjectSerializer
from .views import ProjectUpdateView


#ite.register_module(Project, **{
#   'update': ProjectUpdateView,
#   'permissions': ProjectPermission,
#   'serializer': ProjectSerializer,
#)


#ite.register_dashboards(
#   ProjectManagement(
#       ProjectCategory(
#           ViewFactory(
#               model=Project,
#               name=_("Active projects"),
#               slug="active",
#               manager="active",
#           ),
#           ViewFactory(
#               model=Project,
#               name=_("All projects"),
#               slug="all",
#           ),
#       ),
#   ),
#
