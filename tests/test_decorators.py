#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.test import TestCase
from django.test.utils import override_settings

# from djangobmf.decorators import login_required
from djangobmf.decorators import optional_celery
from djangobmf.conf import settings


class DecoratorTests(TestCase):

    @override_settings(BMF_USE_CELERY=True)
    def test_optional_celery_on(self):
        self.assertEqual(settings.USE_CELERY, True)

        @optional_celery
        def function(arg1, arg2, kwarg1='Test3', kwarg2=4):
            return (arg1, arg2, kwarg1, kwarg2)

        response = function(1, 'Test2', kwarg2=2)

        self.assertEqual(response.result, (1, 'Test2', 'Test3', 2))

    @override_settings(BMF_USE_CELERY=False)
    def test_optional_celery_off(self):
        self.assertEqual(settings.USE_CELERY, False)

        @optional_celery
        def function(arg1, arg2, kwarg1='Test3', kwarg2=4):
            return (arg1, arg2, kwarg1, kwarg2)

        response = function(1, 'Test2', kwarg2=2)

        self.assertEqual(response, (1, 'Test2', 'Test3', 2))
