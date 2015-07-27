#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.template import Context
from django.template.loader import select_template


class Report(object):

    def __init__(self, options=None):
        self.options = options
        self.key = '%s.%s' % (self.__class__.__module__, self.__class__.__name__)

    def get_default_options(self):
        return ''

    def render(self, request, context):
        """
        Dummy render function, reads a template and renders it as html

        returns extension, mime_type, data or file_object, attachment-boolean
        """
        template = select_template(['djangobmf/report_missing.html'])
        return 'html', 'text/html', template.render(Context()), False
