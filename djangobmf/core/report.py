#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.template import Context
from django.template.loader import select_template
# from django.core.exceptions import ImproperlyConfigured
from django.utils import six


class ReportMetaclass(type):
    def __new__(cls, name, bases, attrs):
        super_new = super(ReportMetaclass, cls).__new__
        parents = [
            b for b in bases if isinstance(b, ReportMetaclass) and
            not (b.__name__ == 'NewBase' and b.__mro__ == (b, object))
        ]
        if not parents:
            return super_new(cls, name, bases, attrs)

        # Create the class.
        new_cls = super_new(cls, name, bases, attrs)
        new_cls.key = '%s.%s' % (new_cls.__module__, new_cls.__name__)

        # validation
#       if not hasattr(new_cls, 'model'):
#           raise ImproperlyConfigured('No model attribute defined in %s.' % new_cls)

        return new_cls


class Report(six.with_metaclass(ReportMetaclass, object)):
    """
    """
    manager = None
    date_resolution = None
    permissions = None
    template_name = None

    def __init__(self, options=None):
        self.options = options

    def get_default_options(self):
        return ''

    def render(self, request, context):
        """
        Dummy render function, reads a template and renders it as html

        returns extension, mime_type, data or file_object, attachment-boolean
        """
        template = select_template(['djangobmf/report_missing.html'])
        return 'html', 'text/html', template.render(Context()), False
