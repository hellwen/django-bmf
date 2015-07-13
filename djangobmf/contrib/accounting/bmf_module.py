#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _

from djangobmf.categories import Accounting
from djangobmf.sites import Module
from djangobmf.sites import ViewMixin
from djangobmf.sites import register
from djangobmf.sites import site

from .categories import TransactionCategory
from .models import ACCOUNTING_INCOME
from .models import ACCOUNTING_EXPENSE
from .models import ACCOUNTING_ASSET
from .models import ACCOUNTING_LIABILITY
from .models import Account
from .models import Transaction
from .models import TransactionItem
from .serializers import AccountSerializer
from .serializers import TransactionSerializer
from .serializers import TransactionItemSerializer
from .views import TransactionCreateView
from .views import TransactionUpdateView


@register(dashboard=Accounting)
class AccountModule(Module):
    model = Account
    serializer = AccountSerializer


@register(dashboard=Accounting)
class TransactionModule(Module):
    model = Transaction
    create = TransactionCreateView
    update = TransactionUpdateView
    serializer = TransactionSerializer


@register(dashboard=Accounting)
class TransactionItemModule(Module):
    model = TransactionItem
    serializer = TransactionItemSerializer


site.register_settings('bmfcontrib_accounting', {
    'income': forms.ModelChoiceField(queryset=Account.objects.filter(type=ACCOUNTING_INCOME)),
    'expense': forms.ModelChoiceField(queryset=Account.objects.filter(type=ACCOUNTING_EXPENSE)),
    'customer': forms.ModelChoiceField(queryset=Account.objects.filter(type=ACCOUNTING_ASSET)),
    'supplier': forms.ModelChoiceField(queryset=Account.objects.filter(type=ACCOUNTING_LIABILITY)),
})


@register(category=TransactionCategory)
class AllAccounts(ViewMixin):
    model = Account
    name = _("All Accounts")
    slug = "accounts"


@register(category=TransactionCategory)
class OpenTransactions(ViewMixin):
    model = Transaction
    name = _("Open transactions")
    slug = "open"
    manager = "open"


@register(category=TransactionCategory)
class ClosedTrancations(ViewMixin):
    model = Transaction
    name = _("Closed transactions")
    slug = "closed"
    manager = "closed"
    date_resolution = "month"


@register(category=TransactionCategory)
class Archive(ViewMixin):
    model = TransactionItem
    name = _("Transaction archive")
    slug = "archive"
    date_resolution = "week"
