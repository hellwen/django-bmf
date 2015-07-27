#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.apps import apps
from django.contrib.admin.sites import AlreadyRegistered
from django.core.exceptions import ImproperlyConfigured

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
            if issubclass(cls, ViewMixin):
                if "category" not in self.kwargs:
                    raise ImproperlyConfigured(
                        'You need to define a category, when registering the view %s',
                        cls,
                    )

                category = self.register_category(self.kwargs["category"])
                category.add_view(cls)
                logger.debug('Registered View "%s" to %s', cls.__name__, category.__class__.__name__)

            elif issubclass(cls, Module):
                if "dashboard" not in self.kwargs:
                    raise ImproperlyConfigured(
                        'You need to define a dashbord, when registering the module %s',
                        cls,
                    )

                dashboard = self.register_dashboard(self.kwargs["dashboard"])
                dashboard.add_module(cls)

                # TODO: this code shoule be removed, if the site dependency from modules is removed
                if cls.model in site.modules:
                    raise AlreadyRegistered('The module %s is already registered' % cls.model.__name__)

                site.modules[cls.model] = cls()
                logger.debug('Registered Module "%s"', cls.__name__)

            elif issubclass(cls, Report):
                if "dashboard" not in self.kwargs:
                    raise ImproperlyConfigured(
                        'You need to define a dashbord, when registering the report %s',
                        cls,
                    )
                dashboard = self.register_dashboard(self.kwargs["dashboard"])
                dashboard.add_report(cls)

            else:
                raise ImproperlyConfigured(
                    'You can not register %s with django-bmf',
                    cls,
                )

    __all__ += [
        'register',
        'site',
    ]
