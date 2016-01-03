#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from djangobmf.core.numberrange import NumberRange

class InvoiceNumberRange(NumberRange):
    template = "INV{year}/{month}-{counter:04d}"
    settings = "BMF_INVOICE_NUMBERRANGE"

number_range = InvoiceNumberRange()
