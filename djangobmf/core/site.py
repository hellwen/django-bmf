#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django import forms
from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url
from django.contrib.admin.sites import AlreadyRegistered
from django.contrib.admin.sites import NotRegistered
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured

from djangobmf.core.module import Module
from djangobmf.models import Configuration
from djangobmf.models import NumberCycle

from rest_framework import routers

import logging
logger = logging.getLogger(__name__)


class Site(object):
    """
    Handle modules like the AdminSite from django.contrib.admin.sites
    """

    def __init__(self, namespace=None, app_name=None):
        self.namespace = namespace or "djangobmf"
        self.app_name = app_name or "djangobmf"
        self.router = routers.DefaultRouter()
        self.clear()

    def clear(self):
        # true if the site is active, ie loaded
        self.is_active = False

        # TODO: remove me, if unused
        # self.is_migrated = False

        # combine all registered modules here
        self.modules = {}

        # all currencies should be stored here
        self.currencies = {}

        # all numbercycles are here
        self.numbercycles = []

        # all reports should be stored here
        self.reports = {}

        # all dashboards are stored here
        self.dashboards = []

        # if a module requires a custom setting, it can be stored here
        self.settings = {}
        self.register_settings(self.app_name, {
            'company_name': forms.CharField(
                max_length=100,
                required=True,
            ),
            'company_email': forms.EmailField(
                required=True,
            ),
        })

    def activate(self, test=False):
        # at this point the apps are NOT ready,
        # but we can make database connections

        if self.is_active and not test:  # pragma: no cover
            return True

        logger.debug('Site activation started')

        # ~~~~ numbercycles ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        for model in self.numbercycles:
            ct = ContentType.objects.get_for_model(model)
            count = NumberCycle.objects.filter(ct=ct).count()
            if not count:  # pragma: no branch
                obj = NumberCycle(ct=ct, name_template=model._bmfmeta.number_cycle)
                obj.save()
                logger.debug('Numbercycle for model %s created' % model.__class__.__name__)

        # ~~~~ settings ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        register_settings = list(self.settings.keys())
        for setting in Configuration.objects.all():
            key = '.'.join((setting.app_label, setting.field_name))

            if key in self.settings:
                if not setting.active:
                    setting.active = True
                    setting.save()
                register_settings.remove(key)

            elif setting.active:
                setting.active = False
                setting.save()

        if register_settings:
            logger.debug('Need to register new settings')
            for setting in register_settings:
                app, name = setting.split('.', 1)
                Configuration.objects.create(app_label=app, field_name=name)
                logger.debug('Registered setting %s' % setting)

        # ~~~~ END ~ activate ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        self.is_active = True
        logger.debug('Site is now active')
        return True

    # --- modules -------------------------------------------------------------

    def register_module(self, model, **options):
        if not hasattr(model, '_bmfmeta'):
            raise ImproperlyConfigured(
                'The module %s needs to be an BMF-Model in order to be'
                'registered with django BMF.' % model.__name__
            )
        if model in self.modules:
            raise AlreadyRegistered('The module %s is already registered' % model.__name__)
        self.modules[model] = Module(model, **options)

    def unregister_module(self, module):
        if module not in self.modules:
            raise NotRegistered('The module %s is not registered' % module.__name__)
        del self.modules[module]

    def get_module(self, model):
        return self.modules[model]

    # --- currencies ----------------------------------------------------------

    def register_currency(self, currency):
        if currency.iso in self.currencies:
            raise AlreadyRegistered('The currency %s is already registered' % currency.__name__)
        self.currencies[currency.iso] = currency

    def unregister_currency(self, currency):
        if currency.iso not in self.currencies:
            raise NotRegistered('The currency %s is not registered' % currency.__name__)
        del self.currencies[currency.iso]

    # --- reports -------------------------------------------------------------

    def register_report(self, name, cls):
        if name in self.reports:
            raise AlreadyRegistered('The report %s is already registered' % name)
        self.reports[name] = cls

    def unregister_report(self, name):
        if name not in self.reports:
            raise NotRegistered('The currency %s is not registered' % name)
        del self.reports[name]

    # --- settings ------------------------------------------------------------

    def register_settings(self, app_label, settings_dict):
        for setting_name, field in settings_dict.items():
            self.register_setting(app_label, setting_name, field)

    def register_setting(self, app_label, setting_name, field):
        name = '.'.join([app_label, setting_name])
        if name in self.settings:
            raise AlreadyRegistered('The setting %s is already registered' % name)
        self.settings[name] = field

    def unregister_setting(self, app_label, setting_name):
        name = '.'.join([app_label, setting_name])
        if name not in self.settings:
            raise NotRegistered('The setting %s is not registered' % name)
        del self.settings[name]

    def get_setting_field(self, app_label, setting_name):
        name = '.'.join([app_label, setting_name])
        return self.settings[name]

    # --- number cycle --------------------------------------------------------

    def register_numbercycle(self, model):
        self.numbercycles.append(model)

    # --- dashboards ----------------------------------------------------------

    def get_dashboard(self, key):
        data = [i for i in self.dashboards if i.key == key]
        if len(data) == 1:
            return data[0]
        raise KeyError(key)

    # --- url generation ------------------------------------------------------

    # --- misc methods --------------------------------------------------------

    @property
    def urls(self):
        return self.get_urls(), self.app_name, self.namespace

    @property
    def models(self):
        models = {}
        for model in self.modules.keys():
            ct = ContentType.objects.get_for_model(model)
            models[ct.pk] = model
        return models

    def get_urls(self):

        from djangobmf.urls import urlpatterns

        try:
            ct = ContentType.objects.get_for_model(Configuration)
            self.activate()
        except RuntimeError:
            # During the migrate command, contenttypes are not ready
            # and raise a Runtime error. We ignore that error and return an empty
            # pattern - the urls are not needed during migrations.
            return patterns('')

        for module, data in self.modules.items():
            info = (module._meta.app_label, module._meta.model_name)
            ct = ContentType.objects.get_for_model(module)

            # set the apis
            urlpatterns += patterns(
                '',
                url(
                    r'^api/module/%s/' % ct.pk,
                    include((data.get_api_urls(), self.app_name, "moduleapi_%s_%s" % info))
                ),
            )

            # Skip detail view if the model is marked as a only related model
            if not module._bmfmeta.only_related:
                urlpatterns += patterns(
                    '',
                    url(
                        r'^detail/%s/%s/(?P<pk>[0-9]+)/' % (info[1], info[0]),
                        include((data.get_detail_urls(), self.app_name, "detail_%s_%s" % info))
                    ),
                )
        return urlpatterns
