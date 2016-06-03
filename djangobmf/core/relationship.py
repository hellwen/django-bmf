#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.apps import apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Model
from django.template.loader import select_template
from django.utils import six
from django.utils.translation import ugettext_lazy as _

import re

import logging
logger = logging.getLogger(__name__)


class RelationshipMetaclass(type):
    def __new__(cls, name, bases, attrs):
        super_new = super(RelationshipMetaclass, cls).__new__
        parents = [
            b for b in bases if isinstance(b, RelationshipMetaclass) and
            not (b.__name__ == 'NewBase' and b.__mro__ == (b, object))
        ]
        if not parents:
            return super_new(cls, name, bases, attrs)

        # Create the class.
        new_cls = super_new(cls, name, bases, attrs)

        # validation
        if not getattr(new_cls, 'model_to', None):
            raise ImproperlyConfigured('No model_to attribute defined in %s.' % new_cls)

        try:
            ismodel = issubclass(new_cls.model_to, Model)
        except:
            ismodel = False

        if ismodel:
            new_cls._model_to = new_cls.model_to
        elif hasattr(new_cls, 'settings'):
            new_cls._model_to = apps.get_model(getattr(settings, new_cls.settings, new_cls.model_to))
        else:
            new_cls._model_to = apps.get_model(new_cls.model_to)

        if not getattr(new_cls, 'name', None):
            raise ImproperlyConfigured('No name attribute defined in %s.' % new_cls)

        if not getattr(new_cls, 'slug', None):
            raise ImproperlyConfigured('No slug attribute defined in %s.' % new_cls)

        if not re.match('^[\w-]+$', new_cls.slug):
            raise ImproperlyConfigured('The slug attribute defined in %s contains invalid chars.' % new_cls)

        return new_cls


class RelationshipMixin(object):
    _model_from = None
    settings = None
    template = None
    field = None

    def __eq__(self, other):
        if isinstance(other, Relationship):
            return self._model_to == other._model_to and self.slug == other.slug
        else:
            return False

    def get_html(self):
        templates = self.get_templates()
        return select_template(templates).render({'template': templates[0]})

    def get_templates(self):
        data = []
        if self.template:
            data.append(self.template)
        data.append('%s/%s_bmflist.html' % (
            self._model_from._meta.app_label,
            self._model_from._meta.model_name,
        ))
        data.append('djangobmf/api/list_template_not_found.html')
        return data

    def get_queryset(self, obj):
        raise NotImplementedError(
            'You need to define a get_queryset method '
            'in %s' % self.__class__.__name__
        )

    def filter_queryset(self, request, queryset, view):
        return queryset.all()


class Relationship(six.with_metaclass(RelationshipMetaclass, RelationshipMixin)):
    def get_queryset(self, obj):
        """
        This function resolves the field value to the the queryset provided by
        the django relationship or needs to be overwritten
        """
        if not self.field:
            raise NotImplementedError(
                'You need to define a get_queryset method '
                'or set a field attribute in %s' % self.__class__.__name__
            )
        return getattr(obj, self.field)


class DocumentRelationship(six.with_metaclass(RelationshipMetaclass, RelationshipMixin)):
    name = _('Documents')
    slug = 'documents'

    def get_queryset(self, obj):
        return obj.djangobmf_document
