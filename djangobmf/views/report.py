#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.views.generic import DetailView

from .mixins import ModuleViewPermissionMixin
from .mixins import ModuleViewMixin


class ReportView(ModuleViewPermissionMixin, ModuleViewMixin, DetailView):
    """
    render a report
    """
    content_type = None
    template_name = None
    form_class = None
    export = False
    needs_pk = False

    def get_queryset(self):
        pass

    def get_report_class(self):
        pass

    context_object_name = 'object'

    def get_template_names(self):
        return ["djangobmf/module_report.html"]

    def get(self, request, *args, **kwargs):
        response = super(ModuleReportView, self).get(request, *args, **kwargs)

        ct = ContentType.objects.get_for_model(self.get_object())
        try:
            report = Report.objects.get(contenttype=ct)
            return report.render(self.get_filename(), self.request, self.get_context_data())
        except Report.DoesNotExist:
            # return "no view configured" page
            return response

    def get_filename(self):
        return "report"
