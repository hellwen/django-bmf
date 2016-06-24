#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals


from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from djangobmf.conf import settings as bmfsettings
from djangobmf.models import BMFModel

from .serializers import LocationSerializer


@python_2_unicode_compatible
class AbstractWarehouse(BMFModel):
    """
    """
    name = models.CharField(_("Name"), max_length=255, null=False, blank=False, )
    description = models.TextField(_("Description"), null=True, blank=True, )

    is_active = models.BooleanField(_("Is active"), null=False, blank=False, default=True)

    class Meta(BMFModel.Meta):  # only needed for abstract models
        verbose_name = _('Warehouse')
        verbose_name_plural = _('Warehouses')
        ordering = ['name']
        abstract = True
        permissions = (
            ('can_manage', 'Can manage all locations'),
        )
        swappable = "BMF_CONTRIB_WAREHOUSE"

    class BMFMeta:
        search_fields = ['name']
        has_logging = False
        serializer = LocationSerializer

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class AbstractLocation(BMFModel):
    """
    """
    name = models.CharField(_("Name"), max_length=255, null=False, blank=False, )
    description = models.TextField(_("Description"), null=True, blank=True, )

    warehouse = models.ForeignKey(
        bmfsettings.CONTRIB_WAREHOUSE, null=False, blank=False, related_name='warehouse_locations',
        on_delete=models.CASCADE,
    )

    class Meta(BMFModel.Meta):  # only needed for abstract models
        verbose_name = _('Location')
        verbose_name_plural = _('Locations')
        ordering = ['name']
        abstract = True
        permissions = (
            ('can_manage', 'Can manage all locations'),
        )
        swappable = "BMF_CONTRIB_LOCATION"

    class BMFMeta:
        search_fields = ['name']
        has_logging = False
        serializer = LocationSerializer

    def __str__(self):
        return self.name


class Warehouse(AbstractWarehouse):
    pass


class Location(AbstractLocation):
    pass
