#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.apps import apps
from django.http import Http404

from djangobmf.views.mixins import BaseMixin
from djangobmf.filters import ViewFilterBackend
from djangobmf.pagination import ModulePagination

from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.mixins import DestroyModelMixin


class APIMixin(BaseMixin):

    filter_backends = (ViewFilterBackend,)
    pagination_class = ModulePagination
    paginate_by = 100

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
