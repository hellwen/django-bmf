#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.categories import Sales
from djangobmf.sites import Module
from djangobmf.sites import ViewMixin
from djangobmf.sites import register

from .categories import AddressCategory
from .models import Address
from .serializers import AddressSerializer


@register(dashboard=Sales)
class AddressModule(Module):
    model = Address
    serializer = AddressSerializer


@register(category=AddressCategory)
class AllAccounts(ViewMixin):
    model = Address
    name = _("All Addresses")
    slug = "all"
