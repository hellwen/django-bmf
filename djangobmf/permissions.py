#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.http import Http404

from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS


class AjaxPermission(BasePermission):
    """
    Only allow Ajax requests
    """
    def has_permission(self, request, view):
        return request.is_ajax()

    def has_object_permission(self, request, view, obj):
        return request.is_ajax()


class ModulePermission(BasePermission):
    """
    Permission object to check the module's permissions
    """

    _action = None

    _actions_map = {
        'view': ['%(app_label)s.view_%(model_name)s'],
        'clone': ['%(app_label)s.view_%(model_name)s', '%(app_label)s.clone_%(model_name)s'],
        'create': ['%(app_label)s.view_%(model_name)s', '%(app_label)s.add_%(model_name)s'],
        'update': ['%(app_label)s.view_%(model_name)s', '%(app_label)s.change_%(model_name)s'],
        'delete': ['%(app_label)s.view_%(model_name)s', '%(app_label)s.delete_%(model_name)s'],
    }

    _perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': ['%(app_label)s.view_%(model_name)s'],
        'HEAD': ['%(app_label)s.view_%(model_name)s'],
        'POST': ['%(app_label)s.view_%(model_name)s', '%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.view_%(model_name)s', '%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.view_%(model_name)s', '%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.view_%(model_name)s', '%(app_label)s.delete_%(model_name)s'],
    }

    def _map_perms(method):
        if self._action in self._actions_map:
            return self._actions_map[self._action]
        return self._perms_map[method]

    def _get_default_permissions(self, method, view):
        """
        Given a view and a HTTP method, return the list of permission
        codes that the user is required to have.
        """
        model_cls = getattr(view, 'model', None)
        assert model_cls is not None, (
            'Cannot apply Permissions on a view that '
            'does not have a `model` property.'
        )
        kwargs = {
            'app_label': model_cls._meta.app_label,
            'model_name': model_cls._meta.model_name,
        }
        return [perm % kwargs for perm in self._map_perms(method)]

    def has_permission(self, request, view):
        perms = self._get_default_permissions(request.method, view)
        return request.user.has_perms(perms)

    def has_object_permission(self, request, view, obj):
        perms = self._get_default_permissions(request.method, view)

        # generate a 403 response if the object's state does not allow it to be updated
        if request.method in ["PUT", "PATCH"] or _action in ["update"]:
            if obj._bmfmeta.workflow and not obj._bmfmeta.workflow.object.update:
                return False

        # generate a 403 response if the object's state does not allow it to be deleted
        if request.method in ["DELETE"] or _action in ["delete"]:
            if obj._bmfmeta.workflow and not obj._bmfmeta.workflow.object.delete:
                return False

        if request.user.has_perms(perms, obj):
            return True

        # If the user does not have permissions we need to determine if
        # they have read permissions to see 403, or get a 404 response.

        if request.method in SAFE_METHODS:
            # Read permissions already checked and failed, no need
            # to make another lookup.
            raise Http404

        read_perms = self.get_permissions('GET', view)
        if not request.user.has_perms(read_perms, obj):
            raise Http404

        # Has read permissions - generate 403 response
        return False

    def filter_queryset(self, qs, user):
        return qs


class ModuleViewPermission(ModulePermission):
    _action = 'view'


class ModuleCreatePermission(ModulePermission):
    _action = 'create'


class ModuleClonePermission(ModulePermission):
    _action = 'clone'


class ModuleUpdatePermission(ModulePermission):
    _action = 'update'


class ModuleDeletePermission(ModulePermission):
    _action = 'delete'
