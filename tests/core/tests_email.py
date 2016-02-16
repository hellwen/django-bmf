#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.test import TestCase

from django.template.loader import get_template

from djangobmf.core.email import get_rendered_node
from djangobmf.core.email import EmailMessage


class ClassTests(TestCase):

    def test_get_rendered_node_available(self):
        template = get_template("djangobmf/tests/core/email/get_rendered_node.html")
        self.assertEqual(get_rendered_node(template, 'test', {}), "testing")

    def test_get_rendered_node_unavailable(self):
        template = get_template("djangobmf/tests/core/email/get_rendered_node.html")
        self.assertEqual(get_rendered_node(template, 'undefined', {}), None)

    def test_missing_template_name(self):
        email = EmailMessage(subject="test", body="test")
        self.assertEqual(email.subject, "test")
        self.assertEqual(email.body, "test")

    def test_missing_template(self):
        email = EmailMessage(
            subject="test",
            body="test",
            template_name="djangobmf/tests/core/email/does_not_exist.html",
        )
        self.assertEqual(email.subject, "test")
        self.assertEqual(email.body, "test")

    def test_overwrite_language(self):
        email = EmailMessage(
            template_name="djangobmf/tests/core/email/language.html",
            language='de',
        )
        self.assertEqual(email.subject, "Montag")

    def test_auto_context(self):
        email = EmailMessage(
            subject="test_subject",
            body="test_body",
            template_name="djangobmf/tests/core/email/context.html",
        )
        self.assertEqual(email.subject, "test_subject")
        self.assertEqual(email.body, "test_body")

    def test_body_in_context(self):
        email = EmailMessage(
            subject="test_subject",
            body="test_body",
            template_name="djangobmf/tests/core/email/context.html",
            context={'body': 'body'},
        )
        self.assertEqual(email.subject, "test_subject")
        self.assertEqual(email.body, "body")

    def test_subject_in_context(self):
        email = EmailMessage(
            subject="test_subject",
            body="test_body",
            template_name="djangobmf/tests/core/email/context.html",
            context={'subject': 'subject'},
        )
        self.assertEqual(email.subject, "subject")
        self.assertEqual(email.body, "test_body")

    def test_html_in_template(self):
        email = EmailMessage(
            subject="test",
            body="test",
            template_name="djangobmf/tests/core/email/html_in_template.html",
        )
        self.assertEqual(email.subject, "test")
        self.assertEqual(email.body, "test")
        self.assertEqual(len(email.alternatives), 1)

    def test_subject_in_template(self):
        email = EmailMessage(
            subject="test",
            body="test",
            template_name="djangobmf/tests/core/email/subject_in_template.html",
        )
        self.assertEqual(email.subject, "subjectblock")
        self.assertEqual(email.body, "test")
        self.assertEqual(email.alternatives, [])

    def test_plain_in_template(self):
        email = EmailMessage(
            subject="test",
            body="test",
            template_name="djangobmf/tests/core/email/plain_in_template.html",
        )
        self.assertEqual(email.subject, "test")
        self.assertEqual(email.body, "plainblock")
        self.assertEqual(email.alternatives, [])
