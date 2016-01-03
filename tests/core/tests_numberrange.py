#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.core.exceptions import ImproperlyConfigured
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils.timezone import get_default_timezone

from djangobmf.core.numberrange import NumberRange

import datetime


class ClassTests(TestCase):

    def test_validation_missing_template(self):
        with self.assertRaises(ImproperlyConfigured):
            class Test(NumberRange):
                pass

    def test_validation_missing_counter(self):
        with self.assertRaises(ValidationError):
            class Test(NumberRange):
                template = 'no-counter'

    def test_validation_double_counter(self):
        with self.assertRaises(ValidationError):
            class Test(NumberRange):
                template = '{counter:05d}{counter:05d}'

    def test_validation_month_without_year(self):
        with self.assertRaises(ValidationError):
            class Test(NumberRange):
                template = '{month}{counter:05d}'

    def test_validation_double_month(self):
        with self.assertRaises(ValidationError):
            class Test(NumberRange):
                template = '{month}{month}'

    def test_validation_double_year(self):
        with self.assertRaises(ValidationError):
            class Test(NumberRange):
                template = '{year}{year}'

    def test_validation_wrong_formatter(self):
        with self.assertRaises(ValidationError):
            class Test(NumberRange):
                template = '{wrong}{counter:05d}'

    def test_time_conversion_aware(self):
        class Test(NumberRange):
            template = '{year}-{month}-{counter:05d}'

        nr = Test()
        time = datetime.datetime(1999, 11, 15, 0, 0, 0, tzinfo=get_default_timezone())
        self.assertEqual(nr.from_time(time), datetime.date(1999,11,15))

    def test_time_conversion_native(self):
        class Test(NumberRange):
            template = '{year}-{month}-{counter:05d}'

        nr = Test()
        time = datetime.datetime(1999, 12, 14, 0, 0, 0)
        self.assertEqual(nr.from_time(time), datetime.date(1999,12,14))


    def test_name_range_month(self):
        class Test(NumberRange):
            template = '{year}-{month}-{counter:05d}'

        nr = Test()
        self.assertEqual(nr.type, nr._TYPE_RANGE_MONTH)

        date = datetime.date(1999, 12, 15)
        self.assertEqual(nr.generate_name(date, 2), '1999-12-00002')

        date = datetime.date(1999, 11, 14)
        self.assertEqual(nr.generate_name(date, 1234), '1999-11-01234')

    def test_name_range_year(self):
        class Test(NumberRange):
            template = '{year}-{counter:05d}'

        nr = Test()
        self.assertEqual(nr.type, nr._TYPE_RANGE_YEAR)

        date = datetime.date(1999, 12, 15)
        self.assertEqual(nr.generate_name(date, 2), '1999-00002')

    def test_settings_override(self):
        with self.settings(BMF_NUMBERRANGE_TEST='A{counter:02d}'):
            class Test(NumberRange):
                template = '{counter:05d}'
                settings = 'BMF_NUMBERRANGE_TEST'

        nr = Test()
        date = datetime.date(1999, 12, 15)
        self.assertEqual(nr.generate_name(date, 2), 'A02')

    def test_settings_override_unset(self):
        class Test(NumberRange):
            template = 'B{counter:02d}'
            settings = 'BMF_NUMBERRANGE_TEST'

        nr = Test()
        date = datetime.date(1999, 12, 15)
        self.assertEqual(nr.generate_name(date, 2), 'B02')

    def test_name_counter(self):
        class Test(NumberRange):
            template = '{counter:05d}'
        nr = Test()
        self.assertEqual(nr.type, nr._TYPE_COUNTER)

        date = datetime.date(1999, 12, 15)
        self.assertEqual(nr.generate_name(date, 2), '00002')

    def test_get_period_year(self):
        class Test(NumberRange):
            template = '{counter:05d}'
        date = datetime.date(1999, 10, 15)
        nr = Test()

        nr.type = nr._TYPE_RANGE_YEAR
        i, f = nr.get_period(date)

        self.assertEqual(i, datetime.date(1999, 1, 1))
        self.assertEqual(f, datetime.date(1999, 12, 31))

    def test_get_period_month(self):
        class Test(NumberRange):
            template = '{counter:05d}'
        date = datetime.date(1999, 10, 15)
        nr = Test()

        nr.type = nr._TYPE_RANGE_MONTH
        i, f = nr.get_period(date)

        self.assertEqual(i, datetime.date(1999, 10, 1))
        self.assertEqual(f, datetime.date(1999, 10, 31))
