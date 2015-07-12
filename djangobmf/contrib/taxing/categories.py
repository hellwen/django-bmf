#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.sites import Category


class TaxCategory(Category):
    class Meta:
        name = _('Taxes')
        slug = "taxes"
