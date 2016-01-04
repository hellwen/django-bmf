#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.sites import Module
from djangobmf.sites import ViewMixin
from djangobmf.sites import register

from .categories import TimesheetCategory
from .models import Timesheet
from .permissions import TimesheetPermission
from .views import CreateView
from .views import UpdateView


@register
class TimesheetModule(Module):
    model = Timesheet
    default = True
    create = CreateView
    update = UpdateView
    permissions = TimesheetPermission


@register(category=TimesheetCategory)
class MyTimesheets(ViewMixin):
    model = Timesheet
    name = _("My timesheets")
    slug = "mytimesheets"
    date_resolution = 'week'

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(
            employee=request.user.djangobmf.employee or -1,
        )


@register(category=TimesheetCategory)
class Archive(ViewMixin):
    model = Timesheet
    name = _("Archive")
    slug = "archive"
    date_resolution = 'week'
