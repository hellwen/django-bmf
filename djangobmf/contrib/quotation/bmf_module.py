#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.dashboards import Sales
from djangobmf.sites import Module
from djangobmf.sites import Report
from djangobmf.sites import ViewMixin
from djangobmf.sites import register

from .categories import QuotationCategory
from .models import Quotation
from .models import QuotationProduct
from .serializers import QuotationSerializer
from .views import QuotationCreateView
from .views import QuotationUpdateView


@register(dashboard=Sales)
class QuotationModule(Module):
    model = Quotation
    default = True
    create = QuotationCreateView
    update = QuotationUpdateView
    serializer = QuotationSerializer


@register(dashboard=Sales)
class QuotationProductModule(Module):
    model = QuotationProduct
    default = True


@register(category=QuotationCategory)
class OpenQuotations(ViewMixin):
    model = Quotation
    name = _("Open quotations")
    slug = "open"

    def filter_queryset(self, qs):
        return qs.filter(
            # completed=False,
            state__in=['draft', 'send', 'accepted'],
        )


@register(category=QuotationCategory)
class AllQuotations(ViewMixin):
    model = Quotation
    name = _("All quotations")
    slug = "all"


@register(dashboard=Sales)
class QuotationReport(Report):
    model = QuotationProduct
