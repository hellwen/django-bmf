#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.views.generic.base import TemplateView

from .mixins import ViewMixin


class ModuleOverviewView(ViewMixin, TemplateView):
    template_name = "djangobmf/modules.html"
