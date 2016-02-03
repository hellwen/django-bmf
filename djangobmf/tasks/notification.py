#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.timezone import now

from djangobmf.core.employee import Employee
from djangobmf.decorators import optional_celery

import logging
logger = logging.getLogger(__name__)


@optional_celery
def djangobmf_user_watch(pk):
    from djangobmf.models import Activity
    from djangobmf.models import Notification

    from djangobmf.models import ACTION_COMMENT
    from djangobmf.models import ACTION_CREATED
    from djangobmf.models import ACTION_UPDATED
    from djangobmf.models import ACTION_WORKFLOW
    from djangobmf.models import ACTION_FILE

    object = Activity.objects.get(pk=pk)

    if object.action == ACTION_CREATED:
        logger.debug("Notifications for new object: %s (pk: %s)" % (object.parent_ct, object.parent_id))

        # Select all Notifications not bound to an object

        for notification in Notification.objects \
                .filter(watch_ct=object.parent_ct, watch_id__isnull=True) \
                .select_related('user'):

            # ACL / Permissions lookups
            employee = Employee(notification.user)
            if employee.has_object_perms(object.parent_object):
                notification.pk = None
                if notification.user == object.user:
                    notification.unread = False
                else:
                    notification.unread = True
                notification.new_entry = False
                notification.watch_id = object.parent_id
                notification.last_seen_object = object.pk
                notification.triggered = True
                notification.save()

                logger.debug("Created Notification for user %s (%s) and object %s (%s)" % (
                    notification.user,
                    notification.user.pk,
                    object.parent_ct,
                    object.parent_id,
                ))
    else:
        qs = Notification.objects.filter(watch_ct=object.parent_ct, watch_id=object.parent_id)
        if object.action == ACTION_COMMENT:
            logger.debug("Notifications for comment: %s (pk: %s)" % (object.parent_ct, object.parent_id))
            qs = qs.filter(comments=True)
        if object.action == ACTION_UPDATED:
            logger.debug("Notifications for updated data: %s (pk: %s)" % (object.parent_ct, object.parent_id))
            qs = qs.filter(detectchanges=True)
        if object.action == ACTION_WORKFLOW:
            logger.debug("Notifications for changed workflow: %s (pk: %s)" % (object.parent_ct, object.parent_id))
            qs = qs.filter(workflow=True)
        if object.action == ACTION_FILE:
            logger.debug("Notifications for appended file: %s (pk: %s)" % (object.parent_ct, object.parent_id))
            qs = qs.filter(files=True)

        # ACL
        for notification in qs.select_related('user'):

            employee = Employee(notification.user)
            if employee.has_object_perms(object.parent_object):
                if notification.user != object.user:
                    notification.triggered = True
                    notification.unread = True
                notification.modified = now()
                logger.debug("Updated Notification for user %s (%s) and object %s (%s)" % (
                    notification.user,
                    notification.user.pk,
                    object.parent_ct,
                    object.parent_id,
                ))
            else:
                # User does not have permissions!
                # -> delete notification
                notification.delete()
                logger.info("Deleted Notification for user %s (%s) and object %s (%s) - no permissions" % (
                    notification.user,
                    notification.user.pk,
                    object.parent_ct,
                    object.parent_id,
                ))
