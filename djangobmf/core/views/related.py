#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from rest_framework.exceptions import NotFound
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin

from djangobmf.core.pagination import RelatedPagination
from djangobmf.core.permissions import RelatedPermission
from djangobmf.core.views.mixins import BaseMixin


class View(BaseMixin, ListModelMixin, GenericAPIView):
    permission_classes = [RelatedPermission]
    pagination_class = RelatedPagination

    def get_serializer_class(self):
        if hasattr(self.relation, 'serializer'):
            return getattr(self.relation, 'serializer')
        if hasattr(self.relation._related_model, '_bmfmeta'):
            return self.relation._related_model._bmfmeta.serializer_class
        raise NotImplementedError(
            'You need to use a model managed by djangobmf or '
            'define a serializer attribute on %s' % self.relation.__class__.__name__
        )

    def generate_relation(self):
        if hasattr(self, 'relation') and hasattr(self, 'object'):
            return None
        self.object = self.get_bmfobject(self.kwargs.get('pk', None))
        self.relation = None
        for o in self.request.djangobmf_appconfig.bmf_relations:
            if o._model == self.object.__class__ and o.slug == self.kwargs.get('field', None):
                self.relation = o
                break
        if not self.relation:
            raise NotFound(_("The object's relation can not be found"))

    def get_queryset(self):
        return self.relation.filter_queryset(
            self.request,
            self.relation.get_queryset(self.object),
            self
        )

    def get(self, request, *args, **kwargs):
        response = self.list(request, *args, **kwargs)
        response.data['html'] = self.relation.get_html()
        response.data['model'] = {
            'app_label': self.relation._related_model._meta.app_label,
            'model_name': self.relation._related_model._meta.model_name,
        }
        return response
