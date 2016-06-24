#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.sites import Module
from djangobmf.sites import ViewMixin
from djangobmf.sites import register

from .categories import LocationCategory
from .models import Warehouse
from .models import Location


@register
class WarehouseModule(Module):
    model = Warehouse
    default = True


@register
class LocationModule(Module):
    model = Location
    default = True


@register(category=LocationCategory)
class Warehouses(ViewMixin):
    model = Warehouse
    slug = 'warehouse'
    name = _("Warehouses")


@register(category=LocationCategory)
class Locations(ViewMixin):
    model = Location
    slug = 'location'
    name = _("Locations")
