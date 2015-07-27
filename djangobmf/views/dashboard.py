#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.http import Http404
from django.views.generic import DetailView
# from django.utils import six
# from django.utils.encoding import force_text

from djangobmf.sites import site
from djangobmf.models import Dashboard

from .mixins import ViewMixin


class DashboardView(ViewMixin, DetailView):
    context_object_name = 'object'
    model = Dashboard
    dashboard = None
    template_name = "djangobmf/dashboard/detail.html"

    def get_dashboard(self):
        if "dashboard" in self.kwargs:
            return site.get_dashboard(self.kwargs["dashboard"])
        return None

    def get_object(self):
        if "dashboard" in self.kwargs:
            try:
                self.dashboard = site.get_dashboard(self.kwargs["dashboard"])
            except KeyError:
                raise Http404

        self.object = Dashboard.objects.get_or_create(
            key=self.kwargs.get('dashboard', None)
        )

        return self.object
