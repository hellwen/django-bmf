#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

"""
models doctype
"""

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from djangobmf.currency import Wallet
from djangobmf.fields import CurrencyField
from djangobmf.fields import MoneyField
from djangobmf.models import BMFModel
from djangobmf.settings import CONTRIB_ACCOUNT
from djangobmf.settings import CONTRIB_PROJECT
from djangobmf.settings import CONTRIB_TRANSACTION

from .workflows import TransactionWorkflow

ACCOUNTING_INCOME = 10
ACCOUNTING_EXPENSE = 20
ACCOUNTING_ASSET = 30
ACCOUNTING_LIABILITY = 40
ACCOUNTING_EQUITY = 50

ACCOUNTING_TYPES = (
    (ACCOUNTING_INCOME, _('Income')),
    (ACCOUNTING_EXPENSE, _('Expense')),
    (ACCOUNTING_ASSET, _('Asset')),
    (ACCOUNTING_LIABILITY, _('Liability')),
    (ACCOUNTING_EQUITY, _('Equity')),
)


# =============================================================================
# TODO: Add Fiscal Year
# TODO: Add Period
# =============================================================================


@python_2_unicode_compatible
class BaseAccount(BMFModel):
    """
    Accounts

    ==============  ========  ========
    Account-Type     Credit     Debit
    ==============  ========  ========
    Asset           Decrease  Increase
    Liability       Increase  Decrease
    Income/Revenue  Increase  Decrease
    Expense         Decrease  Increase
    Equity/Capital  Increase  Decrease
    ==============  ========  ========
    """
    parent = models.ForeignKey(
        'self', null=True, blank=True, related_name='child',
        on_delete=models.CASCADE,
    )
    parents = models.ManyToManyField(
        'self', related_name='children', editable=False, symmetrical=False,
    )

    balance_currency = CurrencyField(editable=False)
    balance = MoneyField(editable=False)
    number = models.CharField(_('Number'), max_length=30, null=True, blank=True, unique=True, db_index=True)
    name = models.CharField(_('Name'), max_length=100, null=False, blank=False)
    type = models.PositiveSmallIntegerField(
        _('Type'), null=True, blank=True, choices=ACCOUNTING_TYPES,
    )
    read_only = models.BooleanField(_('Read-only'), default=False)

    def credit_increase(self):
        if self.type in [ACCOUNTING_ASSET, ACCOUNTING_EXPENSE]:
            return False
        else:
            return True

    class Meta:
        verbose_name = _('Account')
        verbose_name_plural = _('Accounts')
        ordering = ['number', 'name', 'type']
        abstract = True
        swappable = "BMF_CONTRIB_ACCOUNT"

    class BMFMeta:
        observed_fields = ['name', ]

    def __init__(self, *args, **kwargs):
        super(BaseAccount, self).__init__(*args, **kwargs)
        self.initial_parent = self.parent_id

    def save(self, update_parents=True, *args, **kwargs):
        super(BaseAccount, self).save(*args, **kwargs)

        if update_parents:
            if self.parent:
                self.parents = list(self.parent.parents.values_list('pk', flat=True)) + [self.parent_id]
            else:
                self.parents = []

        if self.initial_parent != self.parent_id:
            # Update children ...
            for account in Account.objects.filter(parents=self):
                account.save()

    def clean(self):
        if self.parent:
            if not self.type:
                self.type = self.parent.type
            elif self.type != self.parent.type:
                raise ValidationError(_('The type does not match the model parents type'))
        elif not self.type:
            raise ValidationError(_('Root accounts must define a type'))

    def __str__(self):
        return '%s: %s' % (self.number, self.name)


class AbstractAccount(BaseAccount):
    """
    """
    comment = models.TextField(_('Comment'), blank=True, null=True)

    class Meta(BaseAccount.Meta):
        abstract = True

    class BMFMeta(BaseAccount.BMFMeta):
        search_fields = ['name', '^number']


class Account(AbstractAccount):
    """
    """
    pass

# =============================================================================


class BaseTransactionManager(models.Manager):

    def open(self, request):
        return self.get_queryset().filter(
            draft=False,
        ).order_by('-modified')

    def closed(self, request):
        return self.get_queryset().filter(
            draft=True,
        ).order_by('modified')


@python_2_unicode_compatible
class BaseTransaction(BMFModel):
    """
    Transaction
    """
    project = models.ForeignKey(  # TODO optional
        CONTRIB_PROJECT, null=True, blank=True, on_delete=models.SET_NULL,
    )
    text = models.CharField(
        _('Posting text'), max_length=255, null=False, blank=False,
    )
    draft = models.BooleanField(_('Draft'), default=True, editable=False)

#   expensed = models.BooleanField(_('Expensed'), blank=True, null=False, default=False, )

    objects = BaseTransactionManager()

    class Meta:
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')
        abstract = True
        swappable = "BMF_CONTRIB_TRANSACTION"

    class BMFMeta:
        observed_fields = ['expensed', 'text']
        has_files = True
        workflow = TransactionWorkflow

    def __str__(self):
        return '%s' % self.text

    def calc_balance(self):
        if hasattr(self, '_calc_balance'):
            return self._calc_balance

        credit = Wallet()
        debit = Wallet()

        for i in self.items.all():
            if i.credit:
                credit += i.amount
            else:
                debit += i.amount

        self._calc_balance = (credit == debit, credit, debit)
        return self._calc_balance

    def is_balanced(self):
        return self.calc_balance()[0]

    def balance_credit(self):
        return self.calc_balance()[1]

    def balance_debit(self):
        return self.calc_balance()[2]


class Transaction(BaseTransaction):
    """
    """
    pass


class TransactionItemManager(models.Manager):
    """
    """
    def get_queryset(self):
        return super(TransactionItemManager, self).get_queryset() \
            .select_related('account', 'transaction').extra(select={"type": "type"})


class BaseTransactionItem(BMFModel):
    """
    """
    account = models.ForeignKey(
        CONTRIB_ACCOUNT, null=True, blank=False,
        related_name="transactions", on_delete=models.PROTECT,
    )
    transaction = models.ForeignKey(
        CONTRIB_TRANSACTION, null=True, blank=False,
        related_name="items", on_delete=models.CASCADE,
    )

    amount_currency = CurrencyField()
    amount = MoneyField(blank=False)

    credit = models.BooleanField(
        choices=((True, _('Credit')), (False, _('Debit'))),
        default=True,
    )
    draft = models.BooleanField(_('Draft'), default=True, editable=False)

    objects = TransactionItemManager()

    class Meta:
        abstract = True
        swappable = "BMF_CONTRIB_TRANSACTIONITEM"

# def set_debit(self, amount):
#   if self.get_type in [ACCOUNTING_ASSET, ACCOUNTING_EXPENSE]:
#     self.amount =  amount
#   else:
#     self.amount = -amount

# def set_credit(self, amount):
#   if self.get_type in [ACCOUNTING_ASSET, ACCOUNTING_EXPENSE]:
#     self.amount = -amount
#   else:
#     self.amount =  amount

    @property
    def get_type(self):
        try:
            return getattr(self, 'type', self.account.type)
        except AttributeError:
            return 0

# @property
# def is_debit(self):
#   if self.type in [ACCOUNTING_ASSET, ACCOUNTING_EXPENSE]:
#     return self.amount > 0.
#   else:
#     return self.amount < 0.

# @property
# def is_credit(self):
#   return not self.is_debit

# @property
# def get_transation(self):
#   if self.is_debit:
#     return (abs(self.amount), 0)
#   else:
#     return (0, abs(self.amount))


class TransactionItem(BaseTransactionItem):
    """
    This only inherits from AbstractTransactionItem.
    """
    pass
