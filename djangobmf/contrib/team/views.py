#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from djangobmf.views import ModuleCreateView
from djangobmf.views import ModuleUpdateView
from djangobmf.views import ModuleDetail

from .forms import TeamUpdateForm
from .forms import TeamCreateForm


class TeamCreateView(ModuleCreateView):
    form_class = TeamCreateForm


class TeamUpdateView(ModuleUpdateView):
    form_class = TeamUpdateForm

class TeamDetailView(ModuleDetail):
    def get_context_data(self, **kwargs):
        employees = []
        for employee in self.object.employee_set.all():
            employees.append(employee)

        kwargs.update({
            'employees': employees,
        })
        return super(TeamDetailView, self).get_context_data(**kwargs)
