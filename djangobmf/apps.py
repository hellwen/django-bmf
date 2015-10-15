#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.apps import apps
from django.apps import AppConfig
from django.conf import settings
from django.core.checks import register
from django.core.checks import Error
from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import module_has_submodule
from django.utils.module_loading import import_module

from djangobmf.conf import settings as bmfsettings

import logging
logger = logging.getLogger(__name__)


class BMFConfig(AppConfig):
    name = 'djangobmf'
    label = bmfsettings.APP_LABEL
    verbose_name = "Django BMF"

    def ready(self):
        self.bmf_modules = []

        from djangobmf.core.site import Site
        self.site = Site(namespace=self.label, app_name=self.label)


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

            # see if model needs a number_cycle
            for model in [m for m in self.models.values() if hasattr(m, '_bmfmeta') and m._bmfmeta.number_cycle]:
                self.bmf_config.site.register_numbercycle(model)

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
