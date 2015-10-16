#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

# from django.utils import six

# import logging
# logger = logging.getLogger(__name__)


# class FilterQuerysetMetaclass(type):
#    def __new__(cls, name, bases, attrs):
#        super_new = super(FilterQuerysetMetaclass, cls).__new__
#        parents = [
#            b for b in bases if isinstance(b, FilterQuerysetMetaclass) and
#            not (b.__name__ == 'NewBase' and b.__mro__ == (b, object))
#        ]
#        if not parents:
#            return super_new(cls, name, bases, attrs)
#        # Create the class.
#        new_cls = super_new(cls, name, bases, attrs)
#        # validation
#        return new_cls


# class FilterQueryset(six.with_metaclass(FilterQuerysetMetaclass, object)):
class FilterQueryset(object):
    """
    The easiest way to provvide object based access control is via
    a queryset filter. We provide an easy mechanism to add queryset filter
    to your model with the `FilterQueryset` class.
    """

    def __call__(self, queryset, user):
        return self.filter_queryset(queryset, user)

    def filter_queryset(self, queryset, user):
        """
        The filter_queryset method is ment to be overwritten
        """
        return queryset
