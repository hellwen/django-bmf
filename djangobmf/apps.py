#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.apps import apps
from django.apps import AppConfig
from django.conf import settings
from django.contrib.admin.sites import AlreadyRegistered
from django.core.checks import register
from django.core.checks import Error
from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import module_has_submodule
from django.utils.module_loading import import_module

from djangobmf.conf import settings as bmfsettings
from djangobmf.core.relationship import DocumentRelationship

import logging
logger = logging.getLogger(__name__)


class BMFConfig(AppConfig):
    name = 'djangobmf'
    label = bmfsettings.APP_LABEL
    verbose_name = "Django BMF"

    def __init__(self, *args, **kwargs):
        super(BMFConfig, self).__init__(*args, **kwargs)
        self.bmf_modules = {}
        self.bmf_relations = []

    def ready(self):
        from djangobmf.core.site import Site
        self.site = Site(namespace=self.label, app_name=self.label)

    def get_bmfmodule(self, model):
        return self.bmf_modules.get(model, None)

    def register_bmfmodule(self, module):
        return self.bmfregister_module(module)

    def bmfregister_module(self, module):
        """
        register a module with the framework
        """
        if module.model in self.bmf_modules:
            raise AlreadyRegistered(
                'The module %s is already registered' % module.model.__name__
            )

        self.bmf_modules[module.model] = module(self)

        # register files if module has them
        if module.model._bmfmeta.has_files:

            from djangobmf.core.serializers.document import DocumentSerializer

            class FileDownload(DocumentRelationship):
                model = module.model
                serializer = DocumentSerializer

            self.bmfregister_relationship(FileDownload, self.get_model("Document"))

        return self.bmf_modules[module.model]

    def bmfregister_relationship(self, relationship, model):
        r = relationship()
        r._related_model = model
        for obj in self.bmf_relations:
            if obj == r:
                raise AlreadyRegistered(
                    'Can not register the relationship %s' % relationship.__name__
                )
        self.bmf_relations.append(r)

    def bmfregister_list_report(self, report, name):
        if report.model not in self.bmf_modules:
            raise ImproperlyConfigured(
                'Model %s is not registered' % report.model.__class__
            )
        if name in self.bmf_modules[report.model].list_reports:
            raise AlreadyRegistered(
                'Can not register the report %s' % report.__name__
            )
        self.bmf_modules[report.model].list_reports[name] = {
            'class': report,
            'view': report.as_view(),
        }

    def bmfregister_detail_report(self, report, name):
        if report.model not in self.bmf_modules:
            raise ImproperlyConfigured(
                'Model %s is not registered' % report.model.__class__
            )
        if name in self.bmf_modules[report.model].detail_reports:
            raise AlreadyRegistered(
                'Can not register the report %s' % report.__name__
            )
        self.bmf_modules[report.model].detail_reports[name] = {
            'class': report,
            'view': report.as_view(),
        }


class ModuleTemplate(AppConfig):
    bmf_label = bmfsettings.APP_LABEL

    def ready(self):
        # if ready was already called
        if hasattr(self, 'bmf_config'):  # pragma: no cover
            return True

        self.bmf_config = apps.get_app_config(self.bmf_label)

        if not hasattr(self.bmf_config, 'site'):  # pragma: no cover
            raise ImproperlyConfigured(
                "Can not find a site attribute in %(cls)s. "
                "Please import the BMF-Framework before you "
                "import any BMF-Modules in your INSTALLED_APPS." % {
                    'cls': self.bmf_config.__class__.__name__
                }
            )

        # autodiscover bmf modules ============================================
        if module_has_submodule(self.module, "bmf_module"):  # pragma: no branch

            # load instructions of bmf_module.py
            import_module('%s.%s' % (self.name, "bmf_module"))

        logger.debug('App "%s" (%s) is ready' % (
            self.verbose_name,
            self.label,
        ))


class ContribTemplate(ModuleTemplate):
    verbose_name = "Django BMF Contrib"


class CurrencyTemplate(ModuleTemplate):
    verbose_name = "Django BMF Currency"


class ReportTemplate(ModuleTemplate):
    verbose_name = "Django BMF Report"


# Checks
@register()
def checks(app_configs, **kwargs):  # noqa
    errors = []

    if not apps.is_installed('django.contrib.admin'):  # pragma: no cover
        errors.append(Error(
            'django.contrib.admin not found',
            hint="Put 'django.contrib.admin' in your INSTALLED_APPS setting",
            id='djangobmf.E001',
        ))

    if not apps.is_installed('django.contrib.contenttypes'):  # pragma: no cover
        errors.append(Error(
            'django.contrib.contenttypes not found',
            hint="Put 'django.contrib.contenttypes' in your INSTALLED_APPS setting",
            id='djangobmf.E002',
        ))

    if 'django.contrib.auth.context_processors.auth' not in settings.TEMPLATE_CONTEXT_PROCESSORS:  # pragma: no cover
        errors.append(Error(
            'django.contrib.auth.context_processors not found',
            hint="Put 'django.contrib.auth.context_processors' in your TEMPLATE_CONTEXT_PROCESSORS setting",
            id='djangobmf.E003',
        ))

    return errors
