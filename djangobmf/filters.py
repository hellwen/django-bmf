#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from rest_framework.filters import BaseFilterBackend

import logging
logger = logging.getLogger(__name__)


class ViewFilterBackend(BaseFilterBackend):
    """
    """

    def filter_queryset(self, request, queryset, view):
        """
        """
        v = request.GET.get('v', None)
        c = request.GET.get('c', None)
        d = request.GET.get('d', None)

        if not d or not c or not v:
            return queryset

        try:
            parent_view = request.djangobmf_site.get_dashboard(d)[c][v]
        except KeyError:
            return queryset

        if not hasattr(parent_view, 'filter_queryset'):
            return queryset
        return parent_view().filter_queryset(request, queryset, view)
