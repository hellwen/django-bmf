#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.test import TestCase

from djangobmf.core.email import EmailMessage


class ClassTests(TestCase):

    def test_missing_template_name(self):
        email = EmailMessage(subject="test", body="test")
        self.assertEqual(email.subject, "test")
        self.assertEqual(email.body, "test")

    def test_missing_template(self):
        email = EmailMessage(
            subject="test",
            body="test",
            template_base="djangobmf/tests/core/email/does_not_exist",
        )
        self.assertEqual(email.subject, "test")
        self.assertEqual(email.body, "test")

    def test_overwrite_language(self):
        email = EmailMessage(
            template_base="djangobmf/tests/core/email/language",
            language='de',
        )
        self.assertEqual(email.subject, "Montag - Donnerstag")

    def test_auto_context(self):
        email = EmailMessage(
            subject="test_subject",
            body="test_body",
            template_base="djangobmf/tests/core/email/context",
        )
        self.assertEqual(email.subject, "test_subject")
        self.assertEqual(email.body, "test_body")

    def test_body_in_context(self):
        email = EmailMessage(
            subject="test_subject",
            body="test_body",
            template_base="djangobmf/tests/core/email/context",
            context={'body': 'body'},
        )
        self.assertEqual(email.subject, "test_subject")
        self.assertEqual(email.body, "body")

    def test_subject_in_context(self):
        email = EmailMessage(
            subject="test_subject",
            body="test_body",
            template_base="djangobmf/tests/core/email/context",
            context={'subject': 'subject'},
        )
        self.assertEqual(email.subject, "subject")
        self.assertEqual(email.body, "test_body")

    def test_html_mail(self):
        email = EmailMessage(
            subject="test",
            template_base="djangobmf/tests/core/email/mail",
        )
        self.assertEqual(email.subject, "test")
        self.assertEqual(email.body, "HTMLMAIL")
        self.assertEqual(len(email.alternatives), 0)

    def test_html_mail_alternatives(self):
        email = EmailMessage(
            subject="test",
            body="test",
            template_base="djangobmf/tests/core/email/mail",
        )
        self.assertEqual(email.subject, "test")
        self.assertEqual(email.body, "test")
        self.assertEqual(len(email.alternatives), 1)

    def test_html_mail_empty(self):
        email = EmailMessage(
            subject="test",
            body="test",
            template_base="djangobmf/tests/core/email/empty",
        )
        self.assertEqual(email.subject, "test")
        self.assertEqual(email.body, "test")
        self.assertEqual(len(email.alternatives), 0)
