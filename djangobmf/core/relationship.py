#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.apps import apps
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from django.core.exceptions import ValidationError
from django.db.models import Model
from django.utils import six
from django.utils.timezone import get_default_timezone
from django.utils.timezone import is_aware
from django.utils.timezone import localtime

import re
import datetime

import logging
logger = logging.getLogger(__name__)


class RelationshipMetaclass(type):
    def __new__(cls, name, bases, attrs):
        super_new = super(RelationshipMetaclass, cls).__new__
        parents = [
            b for b in bases if isinstance(b, RelationshipMetaclass) and
            not (b.__name__ == 'NewBase' and b.__mro__ == (b, object))
        ]
        if not parents:
            return super_new(cls, name, bases, attrs)

        # Create the class.
        new_cls = super_new(cls, name, bases, attrs)

        # validation
        if not getattr(new_cls, 'model', None):
            raise ImproperlyConfigured('No model attribute defined in %s.' % new_cls)

        if isinstance(new_cls.model, Model):
            new_cls._model = new_cls.model
        elif hasattr(new_cls, 'settings'):
            new_cls._model = apps.get_model(getattr(settings, new_cls.settings, new_cls.model))
        else:
            new_cls._model = apps.get_model(new_cls.model)

        if not getattr(new_cls, 'field', None):
            raise ImproperlyConfigured('No field attribute defined in %s.' % new_cls)

        if not getattr(new_cls, 'template', None):
            raise ImproperlyConfigured('No template attribute defined in %s.' % new_cls)

#       if not getattr(new_cls, 'name', None):
#           raise ImproperlyConfigured('No name attribute defined in %s.' % new_cls)

#       new_cls._model = new_cls.settings and getattr(settings, new_cls.settings, None) or new_cls.template
#       new_cls.validate_template()
#       new_cls.get_type()

        return new_cls


class Relationship(six.with_metaclass(RelationshipMetaclass, object)):
    settings = None

#   pass
#   _MATCH_YEAR = r'{year}'
#   _MATCH_MONTH = r'{month}'
#   _MATCH_COUNTER = r'{counter:0[1-9]+[0-9]*d}'
#   _TYPE_RANGE_MONTH = 'm'
#   _TYPE_RANGE_YEAR = 'y'
#   _TYPE_COUNTER = 'c'
#   lookup = {}
#   def name(self, obj, time_field="created"):
#       ct = ContentType.objects.get_for_model(obj)
#       if self.type == self._TYPE_COUNTER:
#           date = None
#           number = self.get_object(ct)
#           if lookup:
#               counter = obj._base_manager.filter(**lookup).count() + number.counter
#           else:
#               counter = obj.pk
#       else:
#           date = self.from_time(getattr(obj, time_field))
#           number = self.get_object(ct, date)

#           lookup = self.lookup
#           lookup.update({
#               '%s__gte' % time_field: number.period_start,
#               'pk__lt': obj.pk,
#           })

#           counter = obj._base_manager.filter(**lookup).count() + number.counter

#       return self.generate_name(date, counter)

#   def delete(self, obj):
#       ct = ContentType.objects.get_for_model(obj)
#       date = self.from_time(getattr(obj, time_field))

#       number = self.get_object(ct, date)
#       number.counter += 1
#       number.save()

#   def get_object(self, ct, date=None):
#       if self.type == self._TYPE_COUNTER:
#           start = None
#           final = None
#       else:
#           start, final = self.get_period(date)

#       return obj

#   @classmethod
#   def validate_template(self):
#       y = re.findall(self._MATCH_YEAR, self._template)
#       m = re.findall(self._MATCH_MONTH, self._template)
#       c = re.findall(self._MATCH_COUNTER, self._template)

#       if len(y) > 1:
#           raise ValidationError('{year} can only be used once')
#       if len(m) > 1:
#           raise ValidationError('{month} can only be used once')
#       if len(m) == 1 and len(y) == 0:
#           raise ValidationError('{month} can only be used while {year} is present')
#       if len(c) > 1:
#           raise ValidationError('{counter:0Nd} can only be used once')
#       if len(c) == 0:
#           raise ValidationError('{counter:0Nd} must be used once')

#       try:
#           self._template.format(year=1999, month=11, counter=1)
#       except KeyError:
#           raise ValidationError('The string has the wrong format')

#   @classmethod
#   def get_type(self):
#       if (re.search(self._MATCH_MONTH, self._template)):
#           self.type = self._TYPE_RANGE_MONTH
#       elif (re.search(self._MATCH_YEAR, self._template)):
#           self.type = self._TYPE_RANGE_YEAR
#       else:
#           self.type = self._TYPE_COUNTER

#   def from_time(self, time):
#       if is_aware(time):
#           localtime(time, get_default_timezone())
#       return datetime.date(time.year, time.month, time.day)

#   def generate_name(self, date, counter):

#       if self.type == self._TYPE_COUNTER:
#           return self._template.format(counter=counter)

#       date = self.get_period(date, as_range=False)

#       return self._template.format(
#           year=date.strftime('%Y'),
#           month=date.strftime('%m'),
#           counter=counter,
#       )

#   def get_period(self, date, as_range=True):
#       start = date
#       end = date

#       if self.type == self._TYPE_RANGE_MONTH:
#           start = datetime.date(date.year, date.month, 1)
#           if date.month == 12:
#               end = datetime.date(date.year + 1, 1, 1) - datetime.timedelta(1)
#           else:
#               end = datetime.date(date.year, date.month + 1, 1) - datetime.timedelta(1)

#       if self.type == self._TYPE_RANGE_YEAR:
#           start = datetime.date(date.year, 1, 1)
#           end = datetime.date(date.year, 12, 31)

#       if as_range:
#           return start, end
#       return start


#   def __init__(self, site):
#       self.data = OrderedDict()
#       self.site = site
#       self.modules = []
#       self.reports = []

#   def __bool__(self):
#       return bool(self.data)

#   def __nonzero__(self):
#       return self.__bool__()

#   def __len__(self):
#       return len(self.data)

#   def __eq__(self, other):
#       if isinstance(other, Dashboard):
#           return self.key == other.key
#       else:
#           return False

#   def __iter__(self):
#       return self.data.values().__iter__()

#   def __getitem__(self, key):
#       return self.data[key]

#   def __contains__(self, item):
#       if isinstance(item, Category):
#           key = item.key
#       else:
#           key = item
#       return key in self.data
