#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)


class BMFFilterBackend(object):
    """
    """

    # Function name and parameters are identical to the django rest framework
    def filter_queryset(self, request, queryset, view):
        """
        The filter_queryset method is ment to be overwritten
        """
        return queryset
