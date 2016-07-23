#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.sites import register
from djangobmf.sites import Relationship

from .models import StockProduct


@register(model_from=StockProduct)
class StockProductRelationship(Relationship):
    name = _("Products")
    slug = "products"
    field = "stock_products"
    model_to = "djangobmf_stock.Stock"
    settings = "BMF_CONTRIB_STOCK"
