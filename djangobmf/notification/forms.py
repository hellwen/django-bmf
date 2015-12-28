#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django import forms


class FollowForm(forms.Form):
    new_entry = forms.BooleanField(required=False, initial=False)
    glob_comment = forms.BooleanField(required=False, initial=False)
    glob_file = forms.BooleanField(required=False, initial=False)
    glob_changed = forms.BooleanField(required=False, initial=False)
    glob_workflow = forms.BooleanField(required=False, initial=False)
    comment = forms.BooleanField(required=False, initial=False)
    file = forms.BooleanField(required=False, initial=False)
    changed = forms.BooleanField(required=False, initial=False)
    workflow = forms.BooleanField(required=False, initial=False)
