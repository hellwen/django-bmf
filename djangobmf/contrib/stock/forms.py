#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from .models import Stock


class StockInCreateForm(ModelForm):
    class Meta:
        model = Stock
        exclude = ['date', 'employee']


class StockOutCreateForm(ModelForm):
    class Meta:
        model = Stock
        exclude = ['date', 'employee']


class StockInUpdateForm(ModelForm):
    class Meta:
        model = Stock
        exclude = ['date']


class StockOutUpdateForm(ModelForm):
    class Meta:
        model = Stock
        exclude = ['date']


class StockCloneForm(ModelForm):
    class Meta:
        model = Stock
        exclude = []
    copy_stocks = forms.BooleanField(
        label=_("Copy the Stocks"),
        initial=True,
        required=False
    )
    clear_employee = forms.BooleanField(
        label=_("When copying unset the stock's employee"),
        initial=True,
        required=False
    )
