#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.categories import BaseCategory
from djangobmf.categories import ViewFactory
from djangobmf.categories import Sales
from djangobmf.sites import site

from .models import Address
from .serializers import AddressSerializer


#ite.register_module(Address, **{
#   'serializer': AddressSerializer,
#)


#lass AddressCategory(BaseCategory):
#   name = _('Address')
#   slug = "address"


#ite.register_dashboards(
#   Sales(
#       AddressCategory(
#           ViewFactory(
#               model=Address,
#               name=_("All Addresses"),
#               slug="all",
#           ),
#       ),
#   ),
#
