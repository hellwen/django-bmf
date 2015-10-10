#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.apps import apps
from django.http import Http404

from djangobmf.core.employee import Employee
from djangobmf.filters import FilterBackend
from djangobmf.pagination import ModulePagination

from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.mixins import DestroyModelMixin


class APIMixin(object):

    filter_backends = (FilterBackend,)

    @property
    def model(self):
        if getattr(self, '_model', None):
            return self._model

        try:
            self._model = apps.get_model(self.kwargs.get('app'), self.kwargs.get('model'))
        except LookupError:
            raise Http404

        if not hasattr(self._model, '_bmfmeta'):
            raise Http404

        # Connect the requests user to the BMF-Employee model (if installed)
        self.request.user.djangobmf = Employee(self.request.user)

        return self._model

    def get_queryset(self):
        qs = self.model._bmfmeta.filter_queryset(
            self.model.objects.all(),
            self.request.user,
        )
        return qs

    def get_serializer_class(self):
        """
        return the serializer which is registered with the model
        """
        return self.model._bmfmeta.serializer_class


class APIModuleListView(APIMixin, ListModelMixin, CreateModelMixin, GenericAPIView):

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class APIModuleDetailView(APIMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class ModuleListAPIView(ListModelMixin, CreateModelMixin, GenericAPIView):
    """
    """
    model = None
    module = None
    permissions = None
    pagination_class = ModulePagination
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
