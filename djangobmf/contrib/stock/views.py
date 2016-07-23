#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.timezone import now

from djangobmf.views import ModuleCreateView
from djangobmf.views import ModuleUpdateView

from .forms import StockInCreateForm
from .forms import StockOutCreateForm
from .forms import StockInUpdateForm
from .forms import StockOutUpdateForm


class StockInCreateView(ModuleCreateView):
    form_class = StockInCreateForm

    def form_valid(self, form):
        form.instance.date = now()
        form.instance.stock_type = "IN"
        form.instance.employee = self.request.user.djangobmf.employee
        return super(StockInCreateView, self).form_valid(form)


class StockOutCreateView(ModuleCreateView):
    form_class = StockOutCreateForm

    def form_valid(self, form):
        form.instance.date = now()
        form.instance.stock_type = "OUT"
        form.instance.employee = self.request.user.djangobmf.employee
        return super(StockOutCreateView, self).form_valid(form)


class StockUpdateView(ModuleUpdateView):
    def get_form_class(self, *args, **kwargs):

        if self.object.stock_type == "IN":
            return StockInUpdateForm
        else:
            return StockOutUpdateForm
