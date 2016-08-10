#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.sites import register
from djangobmf.sites import Relationship

from .models import ProductTax


@register(model_from=ProductTax)
class ProdictTaxRelationship(Relationship):
    name = _("Taxes")
    slug = "taxes"
    field = "product_tax"
    model_to = "djangobmf_product.Product"
    settings = "BMF_CONTRIB_PRODUCT"
