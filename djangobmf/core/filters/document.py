#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from rest_framework.filters import BaseFilterBackend


class DocumentFilter(BaseFilterBackend):
    """
    """

    def filter_queryset(self, request, queryset, view):
        if view.get_related_object():
            return queryset.filter(
                is_static=False,
                content_type=view.get_bmfcontenttype(),
                content_id=view.related_object.pk,
            )
        else:
            return queryset.filter(
                is_static=True
            )
