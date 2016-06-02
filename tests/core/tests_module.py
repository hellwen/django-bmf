#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.test import TestCase

from djangobmf.core.module import Module
from djangobmf.models import Document


class ModuleTests(TestCase):
    def setUp(self):  # noqa

        class TestModule(Module):
            model = Document

        self.module = TestModule(None)

        super(ModuleTests, self).setUp()

    def test_get_update_view(self):
        # The function is not implemented - the return value should be None
        self.assertEqual(None, self.module.get_update_view())

    def test_get_delete_view(self):
        # The function is not implemented - the return value should be None
        self.assertEqual(None, self.module.get_delete_view())

    def test_get_detail_view(self):
        # TODO
        pass

    def test_serialize_class(self):
        # TODO
        pass

    def test_serialize_object(self):
        # The function is not implemented - the return value should be None
        self.assertEqual({}, self.module.serialize_object(None))

    def test_validate_workflow(self):
        # TODO
        pass

    def test_has_workflow(self):
        # TODO
        pass

    def test_get_workflow_states(self):
        # The function is not implemented - the return value should be None
        self.assertEqual(None, self.module.get_workflow_states(None))

    def test_get_workflow_transitions(self):
        # The function is not implemented - the return value should be None
        self.assertEqual(None, self.module.get_workflow_transitions(None, None))

    def test_get_permissions(self):
        # The function is not implemented - the return value should be None
        self.assertEqual(None, self.module.get_permissions(None))

    def test_has_create_views(self):
        # The function is not implemented - the return value should be None
        self.assertEqual(False, self.module.has_create_views())

    def test_get_create_views(self):
        # The function is not implemented - the return value should be None
        self.assertEqual([], self.module.get_create_views())

    def test_get_create_view(self):
        # The function is not implemented - the return value should be None
        self.assertEqual(None, self.module.get_create_view(None))

    def test_add_create_view(self):
        # The function is not implemented - the return value should be None
        self.assertEqual(None, self.module.add_create_view(None, None))

    def test_has_clone_views(self):
        # The function is not implemented - the return value should be None
        self.assertEqual(False, self.module.has_clone_views())

    def test_get_clone_views(self):
        # The function is not implemented - the return value should be None
        self.assertEqual(None, self.module.get_clone_views())

    def test_get_clone_view(self):
        # The function is not implemented - the return value should be None
        self.assertEqual(None, self.module.get_clone_view(None))

    def test_add_clone_view(self):
        # The function is not implemented - the return value should be None
        self.assertEqual(None, self.module.add_clone_view(None, None))

    def test_add_report(self):
        # TODO
        pass

    def test_get_class_reports(self):
        # The function is not implemented - the return value should be None
        self.assertEqual(None, self.module.get_class_reports())

    def test_get_class_report(self):
        # The function is not implemented - the return value should be None
        self.assertEqual(None, self.module.get_class_report(None))

    def test_add_class_report(self):
        # TODO
        pass

    def test_get_object_reports(self):
        # TODO
        pass

    def test_get_object_report(self):
        # TODO
        pass

    def test_add_object_report(self):
        # TODO
        pass

    def test_get_class_apis(self):
        # The function is not implemented - the return value should be None
        self.assertEqual(None, self.module.get_class_apis())

    def test_get_class_api(self):
        # The function is not implemented - the return value should be None
        self.assertEqual(None, self.module.get_class_api(None))

    def test_add_class_api(self):
        # The function is not implemented - the return value should be None
        self.assertEqual(None, self.module.add_class_api(None, None))

    def test_get_object_apis(self):
        # The function is not implemented - the return value should be None
        self.assertEqual(None, self.module.get_object_apis())

    def test_get_object_api(self):
        # The function is not implemented - the return value should be None
        self.assertEqual(None, self.module.get_object_api(None))

    def test_add_object_api(self):
        # The function is not implemented - the return value should be None
        self.assertEqual(None, self.module.add_object_api(None, None))

    def test_has_relations(self):
        # The function is not implemented - the return value should be False
        self.assertEqual(False, self.module.has_relations())

    def test_get_relations(self):
        # The function is not implemented - the return value should be None
        self.assertEqual(None, self.module.get_relations())

    def test_get_relation(self):
        # The function is not implemented - the return value should be None
        self.assertEqual(None, self.module.get_relation(None))

    def test_add_relation(self):
        # The function is not implemented - the return value should be None
        self.assertEqual(None, self.module.add_relation(None, None))

    def test_has_numberranges(self):
        # The function is not implemented - the return value should be None
        self.assertEqual(None, self.module.has_numberranges())

    def test_get_numberranges(self):
        # The function is not implemented - the return value should be None
        self.assertEqual(None, self.module.get_numberranges())

    def test_get_numberrange(self):
        # The function is not implemented - the return value should be None
        self.assertEqual(None, self.module.get_numberrange(None))

    def test_add_numberrange(self):
        # The function is not implemented - the return value should be None
        self.assertEqual(None, self.module.add_numberrange(None, None))

    def test_signal_pre_delete(self):
        self.assertEqual(None, self.module.signal_pre_delete())

    def test_signal_pre_init(self):
        self.assertEqual(None, self.module.signal_pre_init())

    def test_signal_pre_save(self):
        self.assertEqual(None, self.module.signal_pre_save())

    def test_signal_post_delete(self):
        self.assertEqual(None, self.module.signal_post_delete())

    def test_signal_post_init(self):
        self.assertEqual(None, self.module.signal_post_init())

    def test_signal_post_save(self):
        self.assertEqual(None, self.module.signal_post_save())
