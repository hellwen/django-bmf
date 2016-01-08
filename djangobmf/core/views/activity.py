#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import ListModelMixin

from djangobmf.core.pagination import ActivityPagination
from djangobmf.core.serializers import ActivitySerializer
from djangobmf.core.serializers import NotificationViewSerializer
from djangobmf.models import Activity
from djangobmf.models import Notification
from djangobmf.permissions import ActivityPermission
from djangobmf.views.mixins import BaseMixin


class View(BaseMixin, CreateModelMixin, ListModelMixin, GenericAPIView):
    permission_classes = [ActivityPermission]
    serializer_class = ActivitySerializer
    pagination_class = ActivityPagination

    def get_queryset(self):
        # check if the user has access to the object
        self.get_bmfobject(self.kwargs.get('pk', None))

        return Activity.objects.filter(
            parent_id=self.kwargs.get('pk', None),
            parent_ct=self.get_bmfcontenttype(),
        ).select_related('user')

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # we need to add some data to the request, because the paginator
        # will need the informations to fetch the users notifications
        response = self.list(request, *args, **kwargs)

        ct = self.get_bmfcontenttype()
        pk = self.kwargs.get('pk', None)

        try:
            notification = Notification.objects.get(
                user=self.request.user,
                watch_ct=ct,
                watch_id=pk,
            )
            if notification.unread:
                notification.unread = False
                notification.save()
        except Notification.DoesNotExist:
            notification = Notification(
                user=self.request.user,
                watch_ct=ct,
                watch_id=pk,
            )

        response.data['notification'] = NotificationViewSerializer(notification).data

        return response
