#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.sites import register
from djangobmf.sites import Relationship

from .models import Quotation
from .models import QuotationProduct


@register(model_from=QuotationProduct)
class QuotationProductRelationship(Relationship):
    name = _("Positions")
    slug = "positions"
    field = "quotation_products"
    model_to = "djangobmf_quotation.Quotation"
    settings = "BMF_CONTRIB_QUOTATION"


@register(model_from=Quotation)
class QuotationProjectRelationship(Relationship):
    name = _("Quotations")
    slug = "quotation"
    field = "quotation_set"
    model_to = "djangobmf_project.Project"
    settings = "BMF_CONTRIB_PROJECT"


@register(model_from=Quotation)
class QuotationCustomerRelationship(Relationship):
    name = _("Customers")
    slug = "customer"
    field = "quotation_set"
    model_to = "djangobmf_customer.Customer"
    settings = "BMF_CONTRIB_CUSTOMER"
