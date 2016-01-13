#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

# from django.utils.translation import ugettext_lazy as _

# from rest_framework.exceptions import NotFound
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin

from djangobmf.core.permissions import DetailPermission
from djangobmf.core.views.mixins import BaseMixin


class View(BaseMixin, RetrieveModelMixin, GenericAPIView):
    permission_classes = [DetailPermission]

    def get_serializer_class(self):
        if hasattr(self._model, '_bmfmeta'):
            return self._model._bmfmeta.serializer_class
        raise NotImplementedError(
            'You need to use a model managed by djangobmf or '
            'define a serializer attribute on %s' % self._model.__class__.__name__
        )

    def get(self, request, *args, **kwargs):
        response = self.list(request, *args, **kwargs)
        response.data['html'] = self.relation.get_html()
        response.data['model'] = {
            'app_label': self._model._meta.app_label,
            'model_name': self._model._meta.model_name,
        }
        return response
