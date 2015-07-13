#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.core.exceptions import ImproperlyConfigured
from django.utils import six
from django.utils.text import slugify

from collections import OrderedDict

from .category import Category

import re

import logging
logger = logging.getLogger(__name__)


class DashboardMetaclass(type):
    def __new__(cls, name, bases, attrs):
        super_new = super(DashboardMetaclass, cls).__new__
        parents = [
            b for b in bases if isinstance(b, DashboardMetaclass) and
            not (b.__name__ == 'NewBase' and b.__mro__ == (b, object))
        ]
        if not parents:
            return super_new(cls, name, bases, attrs)

        # Create the class.
        new_cls = super_new(cls, name, bases, attrs)

        # validation
        if not getattr(new_cls, 'name', None):
            raise ImproperlyConfigured('No name attribute defined in %s.' % new_cls)

        if not getattr(new_cls, 'slug', None):
            raise ImproperlyConfigured('No slug attribute defined in %s.' % new_cls)

        # we add a key to add a unique identifier
        # the key is equal to the slug (for now) but this
        # gives us the opportunity to add i18n urls later
        key = getattr(new_cls, 'key', new_cls.slug)
        if re.match(key, r'^[\w-]%'):
            new_cls.key = key
        else:
            new_cls.key = slugify(key)

        return new_cls


class Dashboard(six.with_metaclass(DashboardMetaclass, object)):

    def __init__(self):
        self.data = OrderedDict()
        self.modules = []

    def __bool__(self):
        return bool(self.data)

    def __nonzero__(self):
        return self.__bool__()

    def __len__(self):
        return len(self.data)

    def __eq__(self, other):
        if isinstance(other, Dashboard):
            return self.key == other.key
        else:
            return False

    def __iter__(self):
        return self.data.values().__iter__()

    def __getitem__(self, key):
        return self.data[key]

    def __contains__(self, item):
        if isinstance(item, Category):
            key = item.key
        else:
            key = item
        return key in self.data

    def add_category(self, category):
        """
        Adds a category to the dashboard
        """
        for cat in self.data.values():
            if isinstance(cat, category):
                return cat

        cat = category()
        self.data[cat.key] = cat

        for model in cat.models:
            # module = site.get_module(model)
            # if self not in module.dashboards:
            #     module.dashboards.append(self)
            pass

        logger.debug('Registered Category "%s"', cat.__class__.__name__)
        return cat

    def merge(self, other):
        """
        merges two dashboards
        """
        for category in other.data.values():
            self.add_category(category)
