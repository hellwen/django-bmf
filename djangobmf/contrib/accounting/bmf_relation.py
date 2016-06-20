#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.sites import register
from djangobmf.sites import Relationship

from .models import TransactionItem


@register(model_from=TransactionItem)
class TransactionItemRelationship(Relationship):
    name = _("Items")
    slug = "items"
    field = "items"
    model_to = "djangobmf_accounting.Transaction"
    settings = "BMF_CONTRIB_TRANSACTION"
