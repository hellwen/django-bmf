#!/usr/bin/python
# ex:set fileencoding=utf-8:
# flake8: noqa

from __future__ import unicode_literals

from djangobmf.utils.testcases import DemoDataMixin
from djangobmf.utils.testcases import TestCase
from djangobmf.utils.testcases import ModuleMixin


class StockModuleTests(ModuleMixin, DemoDataMixin, TestCase):

    def test_stock_views(self):
        pass
