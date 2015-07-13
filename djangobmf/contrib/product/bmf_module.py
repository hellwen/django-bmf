#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _

from djangobmf.categories import Sales
from djangobmf.sites import Module
from djangobmf.sites import ViewMixin
from djangobmf.sites import register

from .categories import ProductCategory
from .models import Product
from .models import ProductTax
from .models import PRODUCT_SERVICE
from .serializers import ProductSerializer
from .views import ProductCreateView
from .views import ProductDetailView
from .views import ProductUpdateView


@register(dashboard=Sales)
class ProductModule(Module):
    model = Product
    create = ProductCreateView
    detail = ProductDetailView
    update = ProductUpdateView
    serializer = ProductSerializer


@register(dashboard=Sales)
class ProductTaxModule(Module):
    model = ProductTax


#ite.register_settings('bmfcontrib_product', {
#   'default': forms.ModelChoiceField(queryset=Product.objects.filter(type=PRODUCT_SERVICE)),
#)


@register(category=ProductCategory)
class SellableProducts(ViewMixin):
    model = Product
    name = _("Sellable products")
    slug = "sell"
    manager = "can_sold"


@register(category=ProductCategory)
class PurchaseableProducts(ViewMixin):
    model = Product
    name = _("Purchaseable products")
    slug = "purchase"
    manager = "can_purchased"


@register(category=ProductCategory)
class AllProducts(ViewMixin):
    model = Product
    name = _("All products")
    slug = "all"
