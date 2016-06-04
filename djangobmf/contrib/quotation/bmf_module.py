#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.sites import Module
from djangobmf.sites import PDFReport
from djangobmf.sites import Relationship
from djangobmf.sites import ViewMixin
from djangobmf.sites import register

from .categories import QuotationCategory
from .models import Quotation
from .models import QuotationProduct
from .views import QuotationCreateView
from .views import QuotationUpdateView


@register
class QuotationModule(Module):
    model = Quotation
    open_relation = 'positions'
    create = QuotationCreateView
    update = QuotationUpdateView


@register
class QuotationProductModule(Module):
    model = QuotationProduct


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


@register(category=QuotationCategory)
class OpenQuotations(ViewMixin):
    model = Quotation
    name = _("Open quotations")
    slug = "open"

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(
            # completed=False,
            state__in=['draft', 'send', 'accepted'],
        )


@register(category=QuotationCategory)
class AllQuotations(ViewMixin):
    model = Quotation
    name = _("All quotations")
    slug = "all"


@register(name="quotation")
class QuotationReport(PDFReport):
    model = Quotation
    verbose_name = _('Print Quotation')
    has_object = True
