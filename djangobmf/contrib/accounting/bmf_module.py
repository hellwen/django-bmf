#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _

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
from .views import TransactionCreateView
from .views import TransactionUpdateView


@register
class AccountModule(Module):
    model = Account
    open_relation = 'transactions'


@register
class TransactionModule(Module):
    model = Transaction
    create = TransactionCreateView
    update = TransactionUpdateView
    open_relation = 'items'


@register
class TransactionItemModule(Module):
    model = TransactionItem


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

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(draft=True).order_by('-modified')


@register(category=TransactionCategory)
class ClosedTrancations(ViewMixin):
    model = Transaction
    name = _("Closed transactions")
    slug = "closed"
    date_resolution = "month"

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(draft=False).order_by('modified')


@register(category=TransactionCategory)
class Archive(ViewMixin):
    model = TransactionItem
    name = _("Transaction archive")
    slug = "archive"
    date_resolution = "week"
