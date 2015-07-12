#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

# from django.utils.text import slugify

from djangobmf.views import ModuleListView

# import logging
# logger = logging.getLogger(__name__)


class View(object):
    """
    Object internally used to register modules
    """
    view = ModuleListView

    def __init__(self, dashboard):
      # self.name = name
      # # self.slug = slug
        self.dashboard = dashboard
        self.key = self.slug
      # self.kwargs = kwargs

#       if 'manager' in kwargs and 'queryset' in kwargs:
#           site.get_module(self.model).manager[kwargs['manager']] = kwargs['queryset']
