#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.template import Context
from django.template.loader import select_template
from django.utils import six

from djangobmf.conf import settings
from djangobmf.sites import site
from djangobmf.core.renderer import Renderer
from djangobmf.models import Document

from io import BytesIO

import codecs
import requests


if six.PY3:
    from configparser import RawConfigParser
else:
    from ConfigParser import RawConfigParser

try:
    from xhtml2pdf import pisa
    XHTML2PDF = True
except ImportError:
    XHTML2PDF = False


DEFAULT_OPTS = """
[layout]
size = A4
form = A
letter = True

[letter_page]
margin_right = 10mm
margin_bottom = 40mm
extra = true
extra_right = 10mm
extra_top = 40mm
pdf_background_pk = None

[pages]
margin_right = 10mm
margin_bottom = 15mm
margin_top = 20mm
pdf_background_pk = None

[footer]
right = 10mm
height = 10mm
"""


class Xhtml2PdfReport(Renderer):

    model = "asd"

    def __init__(self, options):
        self.options = RawConfigParser(allow_no_value=True)
        try:
            self.options.read_string(options)
        except AttributeError:
            self.options.readfp(BytesIO(options.encode("UTF-8")))

    def get_default_options(self):
        return DEFAULT_OPTS

    def render(self, request, context):
        model = context['bmfmodule']['model']._meta
        template_name = '%s/%s_htmlreport.html' % (model.app_label, model.model_name)

        pages_file = None
        try:
            bg_pk = self.options.getint('pages', 'pdf_background_pk')
            file = Document.objects.get(pk=bg_pk)
            pages_file = codecs.encode(file.file.read(), 'base64').decode().replace('\n', '')
        except (Document.DoesNotExist, ValueError):
            pass

        letter_file = None
        try:
            bg_pk = self.options.getint('letter_page', 'pdf_background_pk')
            file = Document.objects.get(pk=bg_pk)
            letter_file = codecs.encode(file.file.read(), 'base64').decode().replace('\n', '')
        except (Document.DoesNotExist, ValueError):
            pass

        options = {
            'template_name': template_name,

            'size': self.options.get('layout', 'size'),
            'form': self.options.get('layout', 'form'),
            'letter': self.options.getboolean('layout', 'letter'),

            'template_letter': letter_file,
            'template_pages': pages_file,

            'letter_margin_right': self.options.get('letter_page', 'margin_right'),
            'letter_margin_bottom': self.options.get('letter_page', 'margin_bottom'),
            'letter_extra': self.options.getboolean('letter_page', 'extra'),
            'letter_extra_right': self.options.get('letter_page', 'extra_right'),
            'letter_extra_top': self.options.get('letter_page', 'extra_top'),

            'page_margin_top': self.options.get('pages', 'margin_top'),
            'page_margin_right': self.options.get('pages', 'margin_right'),
            'page_margin_bottom': self.options.get('pages', 'margin_bottom'),

            'footer_height': self.options.get('footer', 'height'),
            'footer_right': self.options.get('footer', 'right'),
        }
        context['options'] = options

        template = select_template([template_name, 'djangobmf/report_html_base.html'])

        # pdf won't be in UTF-8
        html = template.render(Context(context)).encode("ISO-8859-1")

        if settings.REPORTING_SERVER:
            response = requests.post(
                settings.REPORTING_SERVER,
                data=html,
                timeout=5.0,
            )
            return 'pdf', 'application/pdf', response.content, True
        elif XHTML2PDF:
            buffer = BytesIO()
            pdf = pisa.pisaDocument(BytesIO(html), buffer)
            pdf = buffer.getvalue()
            buffer.close()
            return 'pdf', 'application/pdf', pdf, True
        else:
            return 'html', 'text/html', html, False


# site.register_report('xhtml2pdf', Xhtml2PdfReport)
