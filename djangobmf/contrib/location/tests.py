#!/usr/bin/python
# ex:set fileencoding=utf-8:
# flake8: noqa

from __future__ import unicode_literals

from .apps import LocationConfig
from .models import Location

from djangobmf.utils.testcases import DemoDataMixin
from djangobmf.utils.testcases import TestCase
from djangobmf.utils.testcases import ModuleMixin
from djangobmf.utils.testcases import ModuleTestFactory


class LocationFactory(ModuleTestFactory, DemoDataMixin, TestCase):
    app = LocationConfig


class LocationModuleTests(ModuleMixin, DemoDataMixin, TestCase):

    def test_location_views(self):
        self.model = Location
        data = self.autotest_ajax_post('create', kwargs={'key': 'default'}, data={
            'name': "test1",
        })
        obj = self.get_latest_object()
        a = '%s'%obj # check if object name has any errors
