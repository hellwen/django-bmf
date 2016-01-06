#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from rest_framework.permissions import BasePermission as Permission


class BasePermission(Permission):
    pass


class RelatedPermission(BasePermission):

    _methods_map = {
        'GET': ['%(app)s.view_%(model)s'],
        'OPTIONS': ['%(app)s.view_%(model)s'],
        'HEAD': ['%(app)s.view_%(model)s'],
    }

    def _get_default_permissions(self, method, view):
        """
        Given a view and a HTTP method, return the list of permission
        codes that the user is required to have.
        """
        kwargs = {
            'app': view.model._meta.app_label,
            'model': view.model._meta.model_name,
        }
        perms1 = [perm % kwargs for perm in self._methods_map[method]]
        kwargs = {
            'app': view.relation._related_model._meta.app_label,
            'model': view.relation._related_model._meta.model_name,
        }
        perms2 = [perm % kwargs for perm in self._methods_map[method]]
        return perms1 + perms2

    def has_permission(self, request, view):
        view.generate_relation()
        perms = self._get_default_permissions(request.method, view)
        return request.user.has_perms(perms)
