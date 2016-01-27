#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.six import text_type
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import get_language

import pycountry
import gettext as gettext_module


# Translations are cached in a dictionary for every language.
_translations = {}


def gettext(value):
    global _translations

    if not settings.USE_I18N:
        return value

    language = get_language()
    if language not in _translations:
        _translations[language] = gettext_module.translation(
            domain='iso3166',
            localedir=pycountry.LOCALES_DIR,
            languages=[language],
            codeset='utf-8',
            fallback=True,
        )
    return _translations[language].gettext(value)


@python_2_unicode_compatible
class CountryContainer(object):
    """
    """

    def __init__(self, value):
        self.obj = pycountry.countries.get(alpha3=value)

    @property
    def name(self):
        return gettext(self.obj.name)

    @property
    def official_name(self):
        return gettext(self.obj.official_name)

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


class CountryField(models.CharField):
    """
    """
    description = _("Country Field")
    default_error_messages = {
        'invalid_country': _('%(name)s is not a valid 3-char country code'),
    }

    def __init__(self, *args, **kwargs):
        defaults = {
            'blank': False,
            'editable': True,
        }
        defaults.update(kwargs)
        defaults.update({
            'max_length': 3,
            'null': True,
        })
        super(CountryField, self).__init__(**defaults)

    def deconstruct(self):
        name, path, args, kwargs = super(CountryField, self).deconstruct()
        del kwargs["null"]
        del kwargs["max_length"]
        return name, path, args, kwargs

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return None
        return self.string_to_country(value)

    def string_to_country(self, value):
        try:
            return CountryContainer(value)
        except KeyError:
            raise ValidationError(
                self.error_messages['invalid_country'],
                code='invalid_country',
                params={'name': value}
            )

    def to_python(self, value):
        if not value:
            return None

        if isinstance(value, CountryContainer):
            return value

        return self.string_to_country(value)

    def get_prep_value(self, value):
        if isinstance(value, CountryContainer):
            return value.key
        return value

    def value_to_string(self, obj):
        """
        serialization
        """
        value = self.val_from_obj(obj)
        return self.get_prep_value(value)
