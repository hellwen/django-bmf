#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.conf.urls import patterns, url
from django.utils.translation import ugettext_lazy as _

from djangobmf.categories import BaseCategory
from djangobmf.categories import ViewFactory
from djangobmf.categories import Sales
from djangobmf.sites import site

from .models import Position
from .serializers import PositionSerializer
from .views import PositionUpdateView
from .views import PositionCreateView
from .views import PositionAPI


#ite.register_module(Position, **{
#   'create': PositionCreateView,
#   'update': PositionUpdateView,
#   'serializer': PositionSerializer,
#   'api_urlpatterns': patterns(
#       '',
#       url(r'^api/$', PositionAPI.as_view(), name="api"),
#   ),
#)


#lass PositionCategory(BaseCategory):
#   name = _('Positions')
#   slug = "positions"


#ite.register_dashboards(
#   Sales(
#       PositionCategory(
#           ViewFactory(
#               model=Position,
#               name=_("Open Positions"),
#               slug="open",
#               manager="open",
#           ),
#           ViewFactory(
#               model=Position,
#               name=_("All positions"),
#               slug="all",
#               date_resolution="month",
#           ),
#       ),
#   ),
#
