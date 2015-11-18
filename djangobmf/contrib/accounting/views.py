#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from djangobmf.views import ModuleCreateView
from djangobmf.views import ModuleUpdateView

from .forms import TransactionUpdateForm
from .forms import TransactionCreateForm


class TransactionCreateView(ModuleCreateView):
    form_class = TransactionCreateForm

    def form_object_save(self, form):
        super(TransactionCreateView, self).form_object_save(form)

        self.object.items.create(
            account=form.cleaned_data['debit'],
            credit=False,
            amount=form.cleaned_data['amount'],
            date=form.cleaned_data['date'],
        )
        self.object.items.create(
            account=form.cleaned_data['credit'],
            credit=True,
            amount=form.cleaned_data['amount'],
            date=form.cleaned_data['date'],
        )

        self.object.save()

        if form.cleaned_data['draft'] is False:
            self.object.state.transition('balance', self.request.user)


class TransactionUpdateView(ModuleUpdateView):
    form_class = TransactionUpdateForm
