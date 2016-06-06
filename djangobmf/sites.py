#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.apps import apps
from django.core.exceptions import ImproperlyConfigured
# from django.db.models import Model

from djangobmf.conf import settings
from djangobmf.core.relationship import Relationship
from djangobmf.core.category import Category
from djangobmf.core.currency import BaseCurrency
from djangobmf.core.dashboard import Dashboard
from djangobmf.core.module import Module
from djangobmf.core.viewmixin import ViewMixin
# from djangobmf.views.module import ModuleDetail
from djangobmf.views.report import ReportBaseView
from djangobmf.core.site import Site


import logging
logger = logging.getLogger(__name__)


__all__ = [
    'Relationship',
    'Category',
    'Dashboard',
    'Module',
    'PDFReport',
    'ViewMixin',
]


site = Site(namespace=settings.APP_LABEL, app_name=settings.APP_LABEL)


class PDFReport(ReportBaseView):
    renderer_class = apps.get_model(settings.APP_LABEL, "PDFRenderer")


# shortcut to the site instance to provide a simple
# syntax to add the framework to external modules
# please note, that this is only available, when the
# apps are loaded (cause the site does some database
# queries). Importing this to early leads to an exception
# which is a feature and not a bug.

if apps.apps_ready:  # pragma: no branch
    # bmfappconfig = apps.get_app_config(settings.APP_LABEL)
    # site = apps.get_app_config(settings.APP_LABEL).site

    config = apps.get_app_config(settings.APP_LABEL)
    site.config = config

    class register(object):  # noqa
        """
        """

        def __init__(self, cls=None, **kwargs):
            self.kwargs = kwargs
            if cls:
                self.register_generic(cls)

        def __call__(self, cls):
            self.register_generic(cls)

        def register_generic(self, cls):
            # Currency
            if issubclass(cls, BaseCurrency):
                site.register_currency(cls)

            # Module
            elif issubclass(cls, Module):
                config.register_module(cls)

            # Views
            elif issubclass(cls, ViewMixin):
                if "category" not in self.kwargs:
                    raise ImproperlyConfigured(
                        'You need to define a category, when registering the view %s',
                        cls,
                    )
                category = self.register_category(self.kwargs["category"])
                category.add_view(cls)
                logger.debug('Registered View "%s" to %s', cls.__name__, category.__class__.__name__)

            # Relationship
            elif issubclass(cls, Relationship):
                if "model_from" not in self.kwargs:
                    raise ImproperlyConfigured(
                        'You need to define a model_from when registering %s',
                        cls.__name__,
                    )
                config.get_module(cls._model_to).add_relation(cls, self.kwargs["model_from"])

            # Report
            elif issubclass(cls, ReportBaseView):
                module = config.get_module(getattr(cls, "model", None))
                if module:
                    module.add_report(cls)
                else:
                    raise ImproperlyConfigured(
                        '%s needs a model witch is registered with the bmf-framework',
                        cls,
                    )

            # Raise Error
            else:
                raise ImproperlyConfigured(
                    'You can not register %s with django-bmf',
                    cls.__name__,
                )

        def register_category(self, category):
            dashboard = self.register_dashboard(category.dashboard)
            category = dashboard.add_category(category)
            return category

        def register_dashboard(self, dashboard):
            for db in site.dashboards:
                if isinstance(db, dashboard):
                    return db

            # Register and initialize the Dashboard
            db = dashboard(site)
            site.dashboards.append(db)
            logger.debug('Registered Dashboard "%s"', dashboard.__name__)
            return db

    __all__ += [
        'register',
        'site',
    ]
