#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.six import with_metaclass
from django.utils.translation import ugettext_lazy as _

from djangobmf.workflow import WorkflowContainer


class WorkflowField(with_metaclass(models.SubfieldBase, models.CharField)):
    """
    Holds the current state of an Workflow object
    can not be edited
    """
    description = _("Workflow Field")

    def __init__(self, workflow, *args, **kwargs):
        self.workflow = workflow
        defaults = {
            'db_index': True,
            'max_length': 32,
        }
        defaults.update(kwargs)
        defaults.update({
            'blank': True,
            'default': None,
            'editable': False,
            'null': True,
        })
        super(WorkflowField, self).__init__(**defaults)

    def deconstruct(self):
        name, path, args, kwargs = super(WorkflowField, self).deconstruct()
        del kwargs["blank"]
        del kwargs["default"]
        del kwargs["editable"]
        del kwargs["null"]
        kwargs["workflow"] = self.workflow
        return name, path, args, kwargs

    def to_python(self, value):
        if isinstance(value, WorkflowContainer):
            return value
        return WorkflowContainer(self.workflow, value)

    def get_prep_value(self, value):
        if isinstance(value, WorkflowContainer):
            return value.key
        return value

    def value_to_string(self, obj):
        """
        serialization
        """
        value = self._get_val_from_obj(obj)
        return self.get_prep_value(value)

    def clean(self, value, *args, **kwargs):
        if (isinstance(value, WorkflowContainer) and isinstance(value.obj, self.workflow)) \
                or value in self.workflow._states:
            return value
        raise ValidationError(_('The workflow state "%s" is not valid') % value)
