#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.db import models
from django.template.loader import select_template
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from djangobmf.fields import FileField

import codecs

from io import BytesIO

try:
    from xhtml2pdf import pisa
    XHTML2PDF = True
except ImportError:
    XHTML2PDF = False


class BaseRenderer(models.Model):
    """
    """

    class Meta:
        abstract = True

    def get_options(self):
        return {}

    def get_context(self, **context):
        if 'options' not in context:
            context['options'] = self.get_options()
        return context

    def get_template_names(self, context=None):
        if context and "template_name" in context:
            return [context['template_name']]
        return []

    def get_template(self, context=None):
        return select_template(self.get_template_names(context=context) + ['djangobmf/report_missing.html'])

    def render(self, **context):
        return 'html', 'text/html', self.get_template(context).render(self.get_context()), False


@python_2_unicode_compatible
class PDFRenderer(BaseRenderer):
    name = models.CharField(
        verbose_name=_("Name"), max_length=20, blank=False, null=False,
    )

    size = models.CharField(
        verbose_name=_("Size"), max_length=10, blank=False, null=False, default="A4",
    )
    form = models.CharField(
        verbose_name=_("Size"), max_length=10, blank=False, null=False, default="A",
    )
    template_extends = models.CharField(
        verbose_name=_("Template Extends"), max_length=40, blank=True, null=True,
    )

    letter = models.BooleanField(
        verbose_name=_("Letter"), default=True,
    )

    letter_margin_top = models.PositiveIntegerField(
        verbose_name=_("Letter margin top"), blank=True, null=True,
    )
    letter_margin_right = models.PositiveIntegerField(
        verbose_name=_("Letter margin right"), blank=False, null=False, default=40,
    )
    letter_margin_bottom = models.PositiveIntegerField(
        verbose_name=_("Letter margin bottom"), blank=False, null=False, default=10,
    )
    letter_margin_left = models.PositiveIntegerField(
        verbose_name=_("Letter margin left"), blank=True, null=True,
    )
    letter_background = FileField(
        verbose_name=_("Letter background"), null=True, blank=True,
    )

    page_margin_top = models.PositiveIntegerField(
        verbose_name=_("Page margin top"), blank=False, null=False, default=20,
    )
    page_margin_right = models.PositiveIntegerField(
        verbose_name=_("Page margin right"), blank=False, null=False, default=40,
    )
    page_margin_bottom = models.PositiveIntegerField(
        verbose_name=_("Page margin bottom"), blank=False, null=False, default=10,
    )
    page_margin_left = models.PositiveIntegerField(
        verbose_name=_("Page margin left"), blank=True, null=True,
    )
    page_background = FileField(
        verbose_name=_("Page background"), null=True, blank=True,
    )

    # 'letter_footer': True,
    # 'letter_footer_height': 10,
    # 'letter_footer_right': 10,

    # 'letter_extra': False,
    # 'letter_extra_width': 10,
    # 'letter_extra_top': 10,
    # 'letter_extra_right': 10,

    modified = models.DateTimeField(_("Modified"), auto_now=True, editable=False,)

    class Meta:
        verbose_name = _('PDF Renderer')
        verbose_name_plural = _('PDF Renderer')
        get_latest_by = "modified"
        abstract = True

    def __str__(self):
        if self.form or self.size:
            data = []
            if self.size:
                data += [self.size]
            if self.form:
                data += [self.form]
            return '%s (%s)' % (self.name, '-'.join(data))
        return '%s' % self.name

    def get_options(self):
        options = {
            'size': self.size,
            'form': self.form,

            'template_extends': self.template_extends or "djangobmf/base_report.html",

            'letter': self.letter,
            'letter_margin_top': self.letter_margin_top,  # defined by size and form
            'letter_margin_left': self.letter_margin_left,  # defined by size and form
            'letter_margin_right': self.letter_margin_right,
            'letter_margin_bottom': self.letter_margin_bottom,
            'letter_background': None,

            'page_margin_top': self.page_margin_top,
            'page_margin_left': self.page_margin_left,  # defined by size and form
            'page_margin_right': self.page_margin_right,
            'page_margin_bottom': self.page_margin_bottom,
            'page_background': None,
        }

        if self.size == "A4":
            if self.form == "A":
                options['letter_margin_top'] = 87
                options['letter_margin_left'] = 25
                options['page_margin_left'] = 25
                options['address'] = True
                options['address_top'] = 27 + 5
                options['address_left'] = 20
                options['address_height'] = 40
                options['address_width'] = 85

            elif self.form == "B":
                options['letter_margin_top'] = 105
                options['letter_margin_left'] = 25
                options['page_margin_left'] = 25
                options['address'] = True
                options['address_top'] = 45 + 5
                options['address_left'] = 20
                options['address_height'] = 40
                options['address_width'] = 85

        if self.letter and self.letter_background and self.letter_background.file_exists:
            self.letter_background.file.open()
            options['letter_background'] = codecs.encode(
                self.letter_background.file.read(),
                'base64'
            ).decode().replace('\n', '')

        if self.page_background and self.page_background.file_exists:
            self.page_background.file.open()
            options['page_background'] = codecs.encode(
                self.page_background.file.read(),
                'base64'
            ).decode().replace('\n', '')

        return options

    def render(self, **context):
        debug = context.pop('debug', False)
        html = self.get_template(context).render(self.get_context(**context)).encode("ISO-8859-1")

        if XHTML2PDF and not debug:
            buff = BytesIO()
            pdf = pisa.pisaDocument(BytesIO(html), buff)
            pdf = buff.getvalue()
            buff.close()
            return 'pdf', 'application/pdf', pdf, True
        else:
            return 'html', 'text/html', html, False


class CSVRenderer(BaseRenderer):
    class Meta:
        verbose_name = _('CSV Renderer')
        verbose_name_plural = _('CSV Renderer')
        abstract = True
