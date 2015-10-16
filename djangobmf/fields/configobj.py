#!/usr/bin/python
# ex:set fileencoding=utf-8:

'''

from __future__ import unicode_literals

# from django.core.exceptions import ValidationError
from django.db import models
from django.utils.six import with_metaclass
from django.utils.translation import ugettext_lazy as _

from configobj import ConfigObj


class ConfigField(with_metaclass(models.SubfieldBase, models.TextField)):
    """
    Holds and configobj
    """
    description = _("Config Field")

    def __init__(self, config, *args, **kwargs):
        self.config = config
        print(args)
        print(kwargs)

        if callable(config):
            self.generate_config = config

        defaults = {
            'editable': True,
            'blank': True,
            'null': True,
        }
        defaults.update(kwargs)
        defaults.update({
            'db_index': False,
        })
        super(ConfigField, self).__init__(**defaults)

    def deconstruct(self):
        name, path, args, kwargs = super(ConfigField, self).deconstruct()
        del kwargs["db_index"]
        kwargs["config"] = self.config
        return name, path, args, kwargs

    def generate_config(self, instance):
        return self.config

#   def to_python(self, value):
#       if isinstance(value, WorkflowContainer):
#           return value
#       return WorkflowContainer(self.workflow, value)

    def get_prep_value(self, value):
        if isinstance(value, ConfigObj):
            return '\n'.join(value.write())
        return value

    def value_to_string(self, obj):
        """
        serialization
        """
        value = self._get_val_from_obj(obj)
        return self.get_prep_value(value)

#   def clean(self, value, *args, **kwargs):
#       if (isinstance(value, WorkflowContainer) and isinstance(value.obj, self.workflow)) \
#               or value in self.workflow._states:
#           return value
#       raise ValidationError(_('The workflow state "%s" is no valid') % value)

'''
