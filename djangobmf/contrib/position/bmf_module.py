#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.conf.urls import patterns, url
from django.utils.translation import ugettext_lazy as _

from djangobmf.dashboards import Sales
from djangobmf.sites import Module
from djangobmf.sites import ViewMixin
from djangobmf.sites import register

from .categories import PositionCategory
from .models import Position
from .serializers import PositionSerializer
from .views import PositionUpdateView
from .views import PositionCreateView
from .views import PositionAPI


@register(dashboard=Sales)
class PositionModule(Module):
    model = Position
    default = True
    create = PositionCreateView
    update = PositionUpdateView
    serializer = PositionSerializer
    api_urlpatterns = patterns(
        '',
        url(r'^api/$', PositionAPI.as_view(), name="api"),
    )


@register(category=PositionCategory)
class OpenPositions(ViewMixin):
    model = Position
    name = _("Open Positions")
    slug = "open"
    manager = "open"


@register(category=PositionCategory)
class AllPositions(ViewMixin):
    model = Position
    name = _("All positions")
    slug = "all"
    date_resolution = "month"
