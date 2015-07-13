#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.categories import Sales
from djangobmf.sites import Module
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
    create = QuotationCreateView
    update = QuotationUpdateView
    serializer = QuotationSerializer
    report = True


@register(dashboard=Sales)
class QuotationProductModule(Module):
    model = QuotationProduct


@register(category=QuotationCategory)
class OpenQuotations(ViewMixin):
    model = Quotation
    name = _("Open quotations")
    slug = "open"
    manager = "open"


@register(category=QuotationCategory)
class AllQuotations(ViewMixin):
    model = Quotation
    name = _("All quotations")
    slug = "all"
