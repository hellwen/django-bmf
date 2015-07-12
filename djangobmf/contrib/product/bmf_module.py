#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _

from djangobmf.sites import site
from djangobmf.categories import ViewFactory
from djangobmf.categories import Sales

from .models import Product
from .models import ProductTax
from .models import PRODUCT_SERVICE
from .serializers import ProductSerializer
from .views import ProductCreateView
from .views import ProductDetailView
from .views import ProductUpdateView


#ite.register_module(Product, **{
#   'create': ProductCreateView,
#   'detail': ProductDetailView,
#   'update': ProductUpdateView,
#   'serializer': ProductSerializer,
#)


#ite.register_module(ProductTax, **{
#)


#ite.register_settings('bmfcontrib_product', {
#   'default': forms.ModelChoiceField(queryset=Product.objects.filter(type=PRODUCT_SERVICE)),
#)


#ite.register_dashboards(
#   Sales(
#       ProductCategory(
#           ViewFactory(
#               model=Product,
#               name=_("Sellable products"),
#               slug="sell",
#               manager="can_sold",
#           ),
#           ViewFactory(
#               model=Product,
#               name=_("Purchaseable products"),
#               slug="purchase",
#               manager="can_purchased",
#           ),
#           ViewFactory(
#               model=Product,
#               name=_("All products"),
#               slug="all",
#           ),
#       ),
#   ),
#
