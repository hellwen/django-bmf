#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.sites import Module
from djangobmf.sites import ViewMixin
from djangobmf.sites import register

from .categories import TaxCategory
from .models import Tax


@register
class TaxModule(Module):
    model = Tax


@register(category=TaxCategory)
class AllTaxes(ViewMixin):
    model = Tax
    name = _("All Taxes")
    slug = "all"
