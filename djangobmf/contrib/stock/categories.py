#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.dashboards import Warehouse
from djangobmf.sites import Category


class StockCategory(Category):
    name = _('Stock')
    slug = "stocks"
    dashboard = Warehouse
