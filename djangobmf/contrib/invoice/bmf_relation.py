#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.sites import register
from djangobmf.sites import Relationship

from .models import Invoice
from .models import InvoiceProduct


@register(model_from=InvoiceProduct)
class InvoiceProductRelationship(Relationship):
    name = _("Positions")
    slug = "positions"
    field = "invoice_products"
    model_to = "djangobmf_invoice.Invoice"
    settings = "BMF_CONTRIB_INVOICE"


@register(model_from=Invoice)
class InvoiceProjectRelationship(Relationship):
    name = _("Invoices")
    slug = "invoice"
    field = "invoice_set"
    model_to = "djangobmf_project.Project"
    settings = "BMF_CONTRIB_PROJECT"


@register(model_from=Invoice)
class InvoiceCustomerRelationship(Relationship):
    name = _("Invoices")
    slug = "invoice"
    field = "invoice_set"
    model_to = "djangobmf_customer.Customer"
    settings = "BMF_CONTRIB_CUSTOMER"
