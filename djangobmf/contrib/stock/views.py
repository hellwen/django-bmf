#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.timezone import now

from djangobmf.views import ModuleCreateView
from djangobmf.views import ModuleUpdateView

from .forms import StockinCreateForm


class StockinCreateView(ModuleCreateView):
    form_class = StockinCreateForm

    def form_valid(self, form):
        form.instance.date = now()
        form.instance.employee = self.request.user.djangobmf.employee
        return super(StockinCreateView, self).form_valid(form)
