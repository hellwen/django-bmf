#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.sites import Module
from djangobmf.sites import PDFReport
from djangobmf.sites import ViewMixin
from djangobmf.sites import register

from .categories import InvoiceCategory
from .models import Invoice
from .models import InvoiceProduct
from .views import InvoiceCreateView
from .views import InvoiceUpdateView


@register
class InvoiceModule(Module):
    model = Invoice
    default = True
    create = InvoiceCreateView
    update = InvoiceUpdateView


@register
class InvoiceProductModule(Module):
    model = InvoiceProduct
    default = True


@register(category=InvoiceCategory)
class OpenInvoices(ViewMixin):
    model = Invoice
    name = _("Open invoices")
    slug = "open"

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(
            state__in=['draft', 'open'],
        )


@register(category=InvoiceCategory)
class AllInvoices(ViewMixin):
    model = Invoice
    name = _("All invoices")
    slug = "all"
    date_resolution = "month"


@register(slug="invoice")
class InvoiceReport(PDFReport):
    model = Invoice
    has_object = True
