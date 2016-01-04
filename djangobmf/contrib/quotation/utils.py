#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from djangobmf.core.numberrange import NumberRange


class QuotationNumberRange(NumberRange):
    template = "Q{year}/{month}-{counter:04d}"
    settings = "BMF_QUOTATION_NUMBERRANGE"

number_range = QuotationNumberRange()
