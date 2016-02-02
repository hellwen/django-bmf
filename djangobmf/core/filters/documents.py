#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from rest_framework.filters import BaseFilterBackend


class DocumentFilter(BaseFilterBackend):
    """
    """

    def filter_queryset(self, request, queryset, view):
        print(request, queryset, view)
        return queryset
