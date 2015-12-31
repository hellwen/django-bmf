#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.core.exceptions import FieldDoesNotExist
from django.utils.timezone import get_current_timezone

from rest_framework.filters import BaseFilterBackend

import datetime
import logging
logger = logging.getLogger(__name__)


class ViewFilterBackend(BaseFilterBackend):
    """
    filter the queryset accordingly to the queryset of the selected view
    """

    def filter_queryset(self, request, queryset, view):
        v = request.GET.get('v', None)
        c = request.GET.get('c', None)
        d = request.GET.get('d', None)

        # variables not set
        if not d or not c or not v:
            return queryset

        try:
            parent_view = request.djangobmf_site.get_dashboard(d)[c][v]
        except KeyError:
            return queryset

        if not hasattr(parent_view, 'filter_queryset'):
            return queryset
        return parent_view().filter_queryset(request, queryset, view)


class RangeFilterBackend(BaseFilterBackend):
    """
    date range filter
    """

    def filter_queryset(self, request, queryset, view):
        start = request.GET.get('date-start', None)
        end = request.GET.get('date-end', None)
        fieldname = request.GET.get('date-field', None)

        # variables not set
        if not start or not end or not fieldname:
            return queryset

        try:
            queryset.model._meta.get_field(fieldname)
        except FieldDoesNotExist:
            logger.exception('Fieldname is invalid')
            return queryset

        # TODO get timezone from request / user / employee
        tz = get_current_timezone()

        i = datetime.datetime.strptime(start, '%Y-%m-%d').replace(tzinfo=tz)
        f = datetime.datetime.strptime(end, '%Y-%m-%d').replace(tzinfo=tz) + datetime.timedelta(1)

        if i > f:
            logger.critical('Date selection range is inverted, returning unfiltered queryset')
            return queryset

        return queryset.filter(**{'%s__gte' % fieldname: i, '%s__lt' % fieldname: f})
