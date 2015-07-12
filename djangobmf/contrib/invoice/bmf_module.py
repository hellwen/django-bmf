#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.categories import BaseCategory
from djangobmf.categories import ViewFactory
from djangobmf.categories import Accounting
from djangobmf.sites import Module
from djangobmf.sites import site
from djangobmf.sites import register

from .categories import InvoiceCategory
from .models import Invoice
from .models import InvoiceProduct
from .serializers import InvoiceSerializer
from .views import InvoiceCreateView
from .views import InvoiceUpdateView


@register(dashboard=Accounting)
class InvoiceModule(Module):
    model = Invoice
    create = InvoiceCreateView
    update = InvoiceUpdateView
    serializer = InvoiceSerializer
    report = {
        'invoice': True,
    }


@register(dashboard=Accounting)
class InvoiceProductModule(Module):
    model = InvoiceProduct


#ite.register_dashboards(
#   Accounting(
#       InvoiceCategory(
#           ViewFactory(
#               model=Invoice,
#               name=_("Open invoices"),
#               slug="open",
#               manager="open",
#           ),
#           ViewFactory(
#               model=Invoice,
#               name=_("All invoices"),
#               slug="all",
#               date_resolution="month",
#           ),
#       ),
#   ),
#
