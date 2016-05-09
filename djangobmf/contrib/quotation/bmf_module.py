#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.sites import Module
from djangobmf.sites import PDFReport
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
    default = True
    create = QuotationCreateView
    update = QuotationUpdateView


@register
class QuotationProductModule(Module):
    model = QuotationProduct
    default = True


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
    model = QuotationProduct
    has_object = True
