#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.six import text_type
from django.utils.six import with_metaclass
from django.utils.translation import ugettext_lazy as _

import pycountry


@python_2_unicode_compatible
class CountryContainer(object):
    """
    """

    def __init__(self, value):
        try:
            self.obj = pycountry.countries.get(alpha3=value)
        except KeyError:
            raise ValidationError(
                _('The country "%s" is not a valid 3-char country code') % value
            )

    @property
    def name(self):
        return self.obj.name

    @property
    def key(self):
        return self.obj.alpha3

    @property
    def alpha2(self):
        return self.obj.alpha2

    @property
    def alpha3(self):
        return self.obj.alpha3

    def __str__(self):
        return text_type(self.obj.alpha3)

    def __len__(self):
        return 3


class CountryField(with_metaclass(models.SubfieldBase, models.CharField)):
    """
    """
    description = _("Country Field")

    def __init__(self, *args, **kwargs):
        defaults = {
            'blank': False,
            'editable': True,
            'null': True,
        }
        defaults.update(kwargs)
        defaults.update({
            'max_length': 3,
        })
        super(CountryField, self).__init__(**defaults)

    def deconstruct(self):
        name, path, args, kwargs = super(CountryField, self).deconstruct()
        del kwargs["max_length"]
        return name, path, args, kwargs

    def to_python(self, value):
        if not value or isinstance(value, CountryContainer):
            return value

        return CountryContainer(value)

    def get_prep_value(self, value):
        if isinstance(value, CountryContainer):
            return value.key
        return value

    def value_to_string(self, obj):
        """
        serialization
        """
        value = self._get_val_from_obj(obj)
        return self.get_prep_value(value)
