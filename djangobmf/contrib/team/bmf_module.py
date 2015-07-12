#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.sites import site
from djangobmf.categories import ViewFactory
from djangobmf.categories import HumanResources

from .models import Team
from .models import TeamMember
from .serializers import TeamSerializer
from .views import TeamCreateView
from .views import TeamUpdateView


#ite.register_module(Team, **{
#   'create': TeamCreateView,
#   'update': TeamUpdateView,
#   'serializer': TeamSerializer,
#)

#ite.register_module(TeamMember, **{
#)


#ite.register_dashboards(
#   HumanResources(
#       TeamCategory(
#           ViewFactory(
#               model=Team,
#               name=_("All Teams"),
#               slug="all",
#           ),
#       ),
#   ),
#
