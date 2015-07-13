#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.apps import apps
from django.contrib.admin.sites import AlreadyRegistered

from djangobmf.conf import settings
from djangobmf.core.category import Category
from djangobmf.core.dashboard import Dashboard
from djangobmf.core.module import Module
from djangobmf.core.report import Report
from djangobmf.core.viewmixin import ViewMixin

import logging
logger = logging.getLogger(__name__)


__all__ = [
    'Category',
    'Dashboard',
    'Module',
    'Report',
    'ViewMixin',
]


# shortcut to the site instance to provide a simple
# syntax to add the framework to external modules
# please note, that this is only available, when the
# apps are loaded (cause the site does some database
# queries). Importing this to early leads to an exception
# which is a feature and not a bug.
if apps.apps_ready:  # pragma: no branch
    site = apps.get_app_config(settings.APP_LABEL).site

    class register(object):  # noqa
        def __init__(self, cls=None, **kwargs):
            self.kwargs = kwargs
            if cls:
                self.register_generic(cls)

        def __call__(self, cls):
            self.register_generic(cls)

        def register_category(self, category):
            dashboard = self.register_dashboard(category.dashboard)
            category = dashboard.add_category(category)
            return category

        def register_dashboard(self, dashboard):
            for db in site.dashboards:
                if isinstance(db, dashboard):
                    return db

            # Register and initialize the Dashboard
            db = dashboard()
            site.dashboards.append(db)
            logger.debug('Registered Dashboard "%s"', dashboard.__name__)
            return db

        def register_generic(self, cls):
            if "dashboard" in self.kwargs:
                self.register_dashboard(self.kwargs["dashboard"])

                if issubclass(cls, Module):
                    if cls.model in site.modules:
                        raise AlreadyRegistered('The module %s is already registered' % cls.model.__name__)
                    site.modules[cls.model] = cls()
                    logger.debug('Registered Module "%s"', cls.__name__)

            if "category" in self.kwargs:
                category = self.register_category(self.kwargs["category"])

                if issubclass(cls, ViewMixin):
                    category.add_view(cls)
                    logger.debug('Registered View "%s" to %s', cls.__name__, category.__class__.__name__)

    __all__ += [
        'register',
        'site',
    ]
