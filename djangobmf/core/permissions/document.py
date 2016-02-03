#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from rest_framework.permissions import BasePermission

from djangobmf.conf import settings


class DocumentPermission(BasePermission):
    _methods_map_document = {
        'GET': ['%(bmf)s.view_%(document)s'],
        'OPTIONS': ['%(bmf)s.view_%(document)s'],
        'HEAD': ['%(bmf)s.view_%(document)s'],
        'POST': ['%(bmf)s.add_%(document)s'],
        'PUT': ['%(bmf)s.change_%(document)s'],
        'PATCH': ['%(bmf)s.change_%(document)s'],
        'DELETE': ['%(bmf)s.delete_%(document)s'],
    }
    _methods_map_related = {
        'GET': ['%(app)s.view_%(model)s'],
        'OPTIONS': ['%(app)s.view_%(model)s'],
        'HEAD': ['%(app)s.view_%(model)s'],
        'POST': ['%(app)s.view_%(model)s', '%(app)s.addfile_%(model)s'],
        'PUT': ['%(app)s.view_%(model)s', '%(app)s.addfile_%(model)s'],
        'PATCH': ['%(app)s.view_%(model)s', '%(app)s.addfile_%(model)s'],
        'DELETE': ['%(app)s.view_%(model)s'],
    }

    def get_perms(self, request, view):
        related = view.get_related_object()
        kwargs = {
            'bmf': settings.APP_LABEL,
            'document': 'document',
        }
        perms_map = self._methods_map_document[request.method]

        if related:
            perms_map += self._methods_map_related[request.method]
            kwargs.update({
                'app': view.model._meta.app_label,
                'model': view.model._meta.model_name,
            })
        return [perm % kwargs for perm in perms_map]

    def has_permission(self, request, view):
        return request.user.has_perms(self.get_perms(request, view))

    def has_object_permission(self, request, view, obj):
        return request.user.has_perms(self.get_perms(request, view), obj)
