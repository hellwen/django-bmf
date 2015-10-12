#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from rest_framework import pagination
from rest_framework.response import Response


class ModulePagination(pagination.PageNumberPagination):

    def get_paginated_response(self, data):
        return Response({
            'pagination': {
                'next': self.get_next_link(),
                'prev': self.get_previous_link(),
                'count': self.page.paginator.count,
            },
            'items': data,
        })
