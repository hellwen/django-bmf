#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from djangobmf.core.employee import Employee

from rest_framework import pagination
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.mixins import DestroyModelMixin


class ModulePaginationSerializer(pagination.PageNumberPagination):

    def get_paginated_response(self, data):
        return Response({
            'pagination': {
                'next': self.get_next_link(),
                'prev': self.get_previous_link(),
                'count': self.page.paginator.count,
            },
            'items': data,
        })


class APIModuleListView(ListModelMixin, CreateModelMixin, GenericAPIView):
    pass

class APIModuleDetailView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    pass


class ModuleListAPIView(ListModelMixin, CreateModelMixin, GenericAPIView):
    """
    """
    model = None
    module = None
    permissions = None
    pagination_class = ModulePaginationSerializer
    paginate_by = 100

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

#   def post(self, request, *args, **kwargs):
#       return self.create(request, *args, **kwargs)

    def get_queryset(self):
        qs = self.model.objects.all()
        self.request.user.djangobmf = Employee(self.request.user)
        return self.permissions().filter_queryset(
            qs,
            self.request.user,
        )

    def get_permissions(self):
        perms = super(ModuleListAPIView, self).get_permissions()
        return [self.permissions()] + perms


class ModuleDetailAPIView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    """
    """
    model = None
    module = None
    serializer = None
    permissions = None

#   def get(self, request, *args, **kwargs):
#       return self.retrieve(request, *args, **kwargs)

#   def put(self, request, *args, **kwargs):
#       return self.update(request, *args, **kwargs)

#   def patch(self, request, *args, **kwargs):
#       return self.partial_update(request, *args, **kwargs)

#   def delete(self, request, *args, **kwargs):
#       return self.destroy(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.all()
