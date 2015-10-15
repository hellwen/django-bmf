#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.dashboards import Sales
from djangobmf.sites import Module
from djangobmf.sites import ViewMixin
from djangobmf.sites import register

from .categories import CustomerCategory
from .models import Customer
from .serializers import CustomerSerializer
from .views import CustomerCreateView
from .views import CompanyCreateView
from .views import UpdateView


@register(dashboard=Sales)
class CustomerModule(Module):
    model = Customer
    default = True
    serializer = CustomerSerializer
    create = {
        u'company': (_('Company'), CompanyCreateView),
        u'customer': (_('Customer'), CustomerCreateView),
    }
    update = UpdateView


@register(category=CustomerCategory)
class CustomerView(ViewMixin):
    model = Customer
    name = _("Customer")
    slug = "customer"

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(
            is_active=True,
            is_customer=True,
        )


@register(category=CustomerCategory)
class SupplierView(ViewMixin):
    model = Customer
    name = _("Supplier")
    slug = "supplier"

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(
            is_active=True,
            is_supplier=True,
        )


@register(category=CustomerCategory)
class AllView(ViewMixin):
    model = Customer
    name = _("All")
    slug = "all"
