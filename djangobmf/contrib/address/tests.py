#!/usr/bin/python
# ex:set fileencoding=utf-8:
# flake8: noqa

from __future__ import unicode_literals

from .apps import AddressConfig
from .models import Address

from djangobmf.utils.testcases import DemoDataMixin
from djangobmf.utils.testcases import TestCase
from djangobmf.utils.testcases import ModuleMixin
from djangobmf.utils.testcases import ModuleTestFactory


class AddressFactory(ModuleTestFactory, DemoDataMixin, TestCase):
    app = AddressConfig


class AddressModuleTests(ModuleMixin, DemoDataMixin, TestCase):

    def test_urls_user(self):
        """
        """
        self.model = Address

        data = self.autotest_ajax_post('create', kwargs={'key': 'default'}, data={
            'customer': 1,
            'name': 'name',
            'street': 'street 12',
            'zip': '24342',
            'city': 'city',
            'state': 'state',
            'country': 'DEU',
            'is_active': '1',
        })
        self.assertNotEqual(data["object_pk"], 0)

        obj = self.get_latest_object()
        a = '%s'%obj # check if object name has any errors

        self.autotest_ajax_post('delete', kwargs={'pk': obj.pk})
