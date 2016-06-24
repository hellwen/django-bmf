#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.timezone import now

from djangobmf.views import ModuleCreateView
from djangobmf.views import ModuleUpdateView

from .forms import StockinCreateForm


class StockinCreateView(ModuleCreateView):
    form_class = StockinCreateForm

    def get_initial(self):
        self.initial.update({
            'date': now(),
            'employee': self.request.user.djangobmf.employee,
        })
        return super(StockinCreateView, self).get_initial()
