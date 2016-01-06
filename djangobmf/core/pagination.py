#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from djangobmf.core.serializers import NotificationViewSerializer
from djangobmf.pagination import PaginationMixin
from djangobmf.models import Notification


class ActivityPagination(PaginationMixin):
    def get_paginated_response_data(self, data):
        data = super(ActivityPagination, self).get_paginated_response_data(data)
        try:
            notification = Notification.objects.get(
                user=self.request.user,
                watch_ct=self.request.bmf_ct,
                watch_id=self.request.bmf_pk,
            )
            if notification.unread:
                notification.unread = False
                notification.save()
        except Notification.DoesNotExist:
            notification = Notification(
                user=self.request.user,
                watch_ct=self.request.bmf_ct,
                watch_id=self.request.bmf_pk,
            )
        data['notification'] = NotificationViewSerializer(notification).data
        return data
