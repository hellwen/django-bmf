#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)


# Parameters of the filter_queryset are identical to the filter-backends 
# in django rest framework
class FilterBackend(object):
    """
    """

    def filter_queryset(self, request, queryset, view):
        """
        The filter_queryset method is ment to be overwritten
        """
        return queryset
