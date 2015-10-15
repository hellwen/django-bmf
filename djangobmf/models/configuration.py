#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.apps import apps
from django.core.cache import caches
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from djangobmf.conf import settings

import json


CACHE_KEY_TEMPLATE = 'bmfconfig.%s.%s'


class ConfigurationManager(models.Manager):

    def get_by_natural_key(self, app_label, field_name):
        return self.get(app_label=app_label, field_name=field_name)

    def get_setting(self, app, name):
        """
        Returns the current ``Configuration`` based on the app-label and
        the name of the setting. The ``Configuration`` object is cached in the
        bmf default cache connection (which should be shared throughout all instances)
        """
        # We need a database connection, and thus the apps to be ready
        if not apps.ready:  # pragma: no cover
            return None

        cache = caches[settings.CACHE_DEFAULT_CONNECTION]
        key = CACHE_KEY_TEMPLATE % (app, name)
        value = cache.get(key)

        if not value:
            from djangobmf.sites import site

            if not site.is_active:
                return None

            # check if the field exists
            field = site.get_setting_field(app, name)

            object, created = self.get_or_create(app_label=app, field_name=name)

            if created:
                object.value = json.dumps(field.initial)
                object.save()
                value = field.initial

            elif object.value:
                value = json.loads(object.value)

        cache.set(key, value)

        return value


@python_2_unicode_compatible
class Configuration(models.Model):
    """
    Model to store informations about settings
    """

    app_label = models.CharField(
        _("Application"), max_length=100, editable=False, null=True, blank=False,
    )
    field_name = models.CharField(
        _("Fieldname"), max_length=100, editable=False, null=True, blank=False,
    )
    value = models.TextField(_("Value"), null=True, blank=False)
    active = models.BooleanField(_("Active"), null=False, default=True)

    objects = ConfigurationManager()

    class Meta:
        verbose_name = _('Configuration')
        verbose_name_plural = _('Configurations')
        default_permissions = ('change',)
        ordering = ["app_label", "field_name"]
        abstract = True
        unique_together = (('app_label', 'field_name'))

    def remove_cached_value(self):
        """
        removes the cache key to ensure it is reloaded if needed
        """
        cache = caches[settings.CACHE_DEFAULT_CONNECTION]
        key = CACHE_KEY_TEMPLATE % (self.app_label, self.field_name)
        cache.delete(key)

    def save(self, *args, **kwargs):
        super(Configuration, self).save(*args, **kwargs)
        # Cached information will likely be incorrect now.
        self.remove_cached_value()

    def delete(self):
        super(Configuration, self).delete()
        # Cached information will likely be incorrect now.
        self.remove_cached_value()

    @classmethod
    def get_setting(cls, app, name):
        return cls._default_manager.get_setting(app, name)

    def __str__(self):
        return '%s.%s' % (self.app_label, self.field_name)

    @models.permalink
    def get_absolute_url(self):
        return ('djangobmf:configuration', (), {
            "app_label": self.app_label,
            "name": self.field_name,
        })

    def natural_key(self):
        return (self.app_label, self.field_name)

#   def clear_cache(self):
#       """Clears the ``Configuration`` object cache."""
#       cache = caches[settings.CACHE_DEFAULT_CONNECTION]
#       cache.clear()
