#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django import forms

from djangobmf.models import Report


class ReportCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ReportCreateForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Report
        exclude = []


class ReportUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ReportUpdateForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Report
        exclude = []
