#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.categories import ViewFactory
from djangobmf.categories import Sales
from djangobmf.sites import site

from .models import Customer
from .serializers import CustomerSerializer
from .views import CustomerCreateView
from .views import CompanyCreateView
from .views import UpdateView

#ite.register_module(Customer, **{
#   'create': {
#       u'company': (_('Company'), CompanyCreateView),
#       u'customer': (_('Customer'), CustomerCreateView),
#   },
#   'update': UpdateView,
#   'serializer': CustomerSerializer,
#)


#ite.register_dashboards(
#   Sales(
#       CustomerCategory(
#           ViewFactory(
#               model=Customer,
#               name=_("Customer"),
#               slug="customer",
#               manager="customer",
#           ),
#           ViewFactory(
#               model=Customer,
#               name=_("Supplier"),
#               slug="supplier",
#               manager="supplier",
#           ),
#           ViewFactory(
#               model=Customer,
#               name=_("All"),
#               slug="all",
#           ),
#       ),
#   ),
#
