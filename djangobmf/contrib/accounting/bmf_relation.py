#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.sites import register
from djangobmf.sites import Relationship

from .models import TransactionItem


@register(model_from=TransactionItem)
class AccountTransactionsRelationship(Relationship):
    name = _("Transactions")
    slug = "transactions"
    field = "transactions"
    model_to = "djangobmf_accounting.Account"
    settings = "BMF_CONTRIB_ACCOUNT"
