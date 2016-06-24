#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.sites import Module
from djangobmf.sites import ViewMixin
from djangobmf.sites import register

from .categories import StockCategory
from .models import Stock
from .models import StockProduct
from .views import StockinCreateView


@register
class StockModule(Module):
    model = Stock
    default = True
    create = StockinCreateView


@register
class StockProductModule(Module):
    model = StockProduct


@register(category=StockCategory)
class Stockin(ViewMixin):
    model = Stock
    slug = 'stockin'
    name = _("Stock In")

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(
            completed=False,
            employee=request.user.djangobmf.employee,
        )


@register(category=StockCategory)
class Stockout(ViewMixin):
    model = Stock
    slug = 'stockout'
    name = _("Stock Out")

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(
            completed=False,
            employee=request.user.djangobmf.employee,
        )


@register(category=StockCategory)
class Stock(ViewMixin):
    model = Stock
    slug = 'stock'
    name = _("Stock")

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(
            completed=False,
            employee=request.user.djangobmf.employee,
        )
