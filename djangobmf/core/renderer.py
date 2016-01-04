#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.template import Context
from django.template.loader import select_template
# from django.core.exceptions import ImproperlyConfigured
from django.utils import six


class RendererMetaclass(type):
    def __new__(cls, name, bases, attrs):
        super_new = super(RendererMetaclass, cls).__new__
        parents = [
            b for b in bases if isinstance(b, RendererMetaclass) and
            not (b.__name__ == 'NewBase' and b.__mro__ == (b, object))
        ]
        if not parents:
            return super_new(cls, name, bases, attrs)

        # Create the class.
        new_cls = super_new(cls, name, bases, attrs)

        # validation
        return new_cls


class Renderer(six.with_metaclass(RendererMetaclass, object)):
    """
    """

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
