#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.apps import apps
from django.apps import AppConfig
from django.conf import settings
from django.contrib.admin.sites import AlreadyRegistered
from django.core.checks import register
from django.core.checks import Error
# from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import module_has_submodule
from django.utils.module_loading import import_module

from djangobmf.conf import settings as bmfsettings


import logging
logger = logging.getLogger(__name__)


class BMFConfig(AppConfig):
    name = 'djangobmf'
    label = bmfsettings.APP_LABEL
    verbose_name = "Django BMF"

    def __init__(self, *args, **kwargs):
        super(BMFConfig, self).__init__(*args, **kwargs)
        self._modules = {}
        self._dashboard = {}

    def ready(self):
        # Autoloader
        for module in ['bmf_module', 'bmf_relation']:
            for app_config in apps.get_app_configs():
                # app_config.bmfconfig = self
                try:
                    import_module('%s.%s' % (app_config.name, module))
                except:
                    if module_has_submodule(app_config.module, module):
                        raise

    def get_module(self, model):
        """
        returs a module instance when called with a model class
        """
        try:
            return self._modules[model]
        except:
            print(list([i.__class__.__name__ for i in self._modules.values()]))
            raise

    def has_module(self, model):
        """
        returs a module instance when called with a model class
        """
        return model in self._modules

    def register_module(self, module):
        """
        register a module with the framework
        """
        if self.has_module(module.model):
            raise AlreadyRegistered(
                'The module %s is already registered' % module.model.__name__
            )
        self._modules[module.model] = module(self)


class ModuleTemplate(AppConfig):
    pass

#   bmf_label = bmfsettings.APP_LABEL

#   def ready(self):
#       # if ready was already called
#       if hasattr(self, 'bmf_config'):  # pragma: no cover
#           return True

#       self.bmf_config = apps.get_app_config(self.bmf_label)

#       if not hasattr(self.bmf_config, 'site'):  # pragma: no cover
#           raise ImproperlyConfigured(
#               "Can not find a site attribute in %(cls)s. "
#               "Please import the BMF-Framework before you "
#               "import any BMF-Modules in your INSTALLED_APPS." % {
#                   'cls': self.bmf_config.__class__.__name__
#               }
#           )

#       # autodiscover bmf modules ============================================
#       if module_has_submodule(self.module, "bmf_module"):  # pragma: no branch

#           # load instructions of bmf_module.py
#           import_module('%s.%s' % (self.name, "bmf_module"))

#       logger.debug('App "%s" (%s) is ready' % (
#           self.verbose_name,
#           self.label,
#       ))


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
