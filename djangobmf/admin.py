#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.contrib import admin

from djangobmf.models import Configuration
from djangobmf.models import Document
from djangobmf.models import Report
from djangobmf.models import PDFRenderer

from djangobmf.forms import ReportCreateForm
from djangobmf.forms import ReportUpdateForm


admin.site.register(Configuration)
admin.site.register(PDFRenderer)


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('name', 'contenttype', 'renderer_ct', 'enabled', 'has_object')
    list_filter = ('enabled', 'has_object')

    def get_form(self, request, obj=None, **kwargs):
        if obj:
            return ReportUpdateForm
        else:
            return ReportCreateForm


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'mimetype', 'size', 'sha1', 'is_static', 'content_type')
    list_display_links = ('name',)
    list_filter = ('modified', 'content_type', 'is_static')
    search_fields = ['name', 'description']
