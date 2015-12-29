#!/usr/bin/python
# ex:set fileencoding=utf-8:
# flake8: noqa

from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse

from djangobmf.models import Activity
from djangobmf.models import ACTION_UPDATED
from djangobmf.models import Notification
from djangobmf.signals import activity_create
from djangobmf.signals import activity_update
from djangobmf.utils.testcases import TestCase
from djangobmf.utils.testcases import ModuleMixin

from .models import TestView

from unittest import expectedFailure


class NotificationTests(ModuleMixin, TestCase):
    model = TestView

    def setUp(self):  # noqa
        super(NotificationTests, self).setUp()

        self.ct = ContentType.objects.get_for_model(TestView)

        self.user1 = self.create_user("user1", is_superuser=True)
        self.user2 = self.create_user("user2", is_superuser=True)

    def prepare_model_tests(self):
        fields = {
            'watch_ct': self.ct,
            'watch_id': None,
            'new_entry': True,
            'comments': True,
            'files': True,
            'detectchanges': True,
            'workflow': True,
        }
        Notification.objects.create(user=self.user1, **fields)
        Notification.objects.create(user=self.user2, **fields)

        self.client_login("user2")

    def test_model_create(self):
        self.prepare_model_tests()
        obj = TestView.objects.create(field="b")
        activity_create.send(sender=obj.__class__, instance=obj)

        self.assertEqual(Notification.objects.filter(watch_ct=self.ct, watch_id=obj.pk).count(), 2, "Counting notification objects")

    @expectedFailure
    def test_model_comment(self):
        self.prepare_model_tests()
        self.assertEqual(1, 0, "not implemented")

    @expectedFailure
    def test_model_file(self):
        self.prepare_model_tests()
        self.assertEqual(1, 0, "not implemented")

    def test_model_changed(self):
        self.prepare_model_tests()
        obj = TestView.objects.create(field="b")
        activity_create.send(sender=obj.__class__, instance=obj)  # TODO: check why we need this

        obj.field = "a"
        activity_update.send(sender=obj.__class__, instance=obj)

        data = Activity.objects.get(parent_ct=self.ct, parent_id=obj.pk, action=ACTION_UPDATED)

        self.assertEqual(
            data.text,
            '[["field", "b", "a"]]',
            "Validation Activity object",
        )

    @expectedFailure
    def test_model_workflow(self):
        self.prepare_model_tests()
        self.assertEqual(1, 0, "not implemented")

    def test_notification_views_index(self):
        """
        """
        self.client_login("user1")

        r = self.client.get(reverse('djangobmf:notification'))
        self.assertEqual(r.status_code, 200)

        r = self.client.get(reverse('djangobmf:notification', kwargs={"filter": "all"}))
        self.assertEqual(r.status_code, 200)

        r = self.client.get(reverse('djangobmf:notification', kwargs={"filter": "active"}))
        self.assertEqual(r.status_code, 200)

        self.assertEqual(Notification.objects.filter(user=self.user1).count(), 0)

        r = self.client.get(reverse('djangobmf:notification', kwargs={'ct': self.ct.pk, "filter": "all"}))
        self.assertEqual(r.status_code, 200)

        # self.assertEqual(Notification.objects.filter(user=self.user1).count(), 1)  # ???

        r = self.client.get(reverse('djangobmf:notification', kwargs={'ct': self.ct.pk, "filter": "active"}))
        self.assertEqual(r.status_code, 200)

        r = self.client.get(reverse('djangobmf:notification', kwargs={'ct': self.ct.pk, "filter": "unread"}))
        self.assertEqual(r.status_code, 200)

    def test_notification_views_edit_root(self):
        self.client_login("user1")
        fields = {
            'user': self.user1,
            'watch_ct': self.ct,
            'watch_id': 0,
        }
        notification = Notification.objects.create(**fields)

        self.assertFalse(notification.new_entry)
        self.assertFalse(notification.comments)
        self.assertFalse(notification.files)
        self.assertFalse(notification.detectchanges)
        self.assertFalse(notification.workflow)

#   def test_notification_views_edit_object(self):
#       self.client_login("user1")
#       obj = TestView.objects.create(field="a")

#       data = self.autotest_ajax_get(
#           url=reverse('djangobmf:notification-create', kwargs={'ct': self.ct.pk, 'pk': obj.pk}),
#       )

#       data = self.autotest_ajax_post(
#           url=reverse('djangobmf:notification-create', kwargs={'ct': self.ct.pk, 'pk': obj.pk}),
#           data={
#               'new_entry': True,
#               'comment': True,
#               'file': True,
#               'changed': True,
#               'workflow': True,
#           }
#       )
#       notification = Notification.objects.get(**{
#           'user': self.user1,
#           'watch_ct': self.ct,
#           'watch_id': obj.pk,
#       })
#       self.assertFalse(notification.new_entry)
#       self.assertTrue(notification.comments)
#       self.assertTrue(notification.files)
#       self.assertTrue(notification.detectchanges)
#       self.assertTrue(notification.workflow)

    def test_models(self):
        pass

    def test_tasks(self):
        pass
