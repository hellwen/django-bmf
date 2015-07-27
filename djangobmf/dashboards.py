#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.sites import Dashboard


__all__ = [
    'Accounting',
    'CustomerRelationship',
    'DocumentManagement',
    'HumanResources',
    'ProjectManagement',
    'Sales',
    'TimeAndAttendance',
    'Warehouse',
]


# --- Predefined Dashboards ---------------------------------------------------


class Accounting(Dashboard):
    name = _('Accounting')
    slug = "accounting"


class CustomerRelationship(Dashboard):
    name = _('Customer Relationship')
    slug = "cr"


class DocumentManagement(Dashboard):
    name = _('Document Management')
    slug = "dms"


class HumanResources(Dashboard):
    name = _('Human Resources')
    slug = "hr"


class ProjectManagement(Dashboard):
    name = _('Project Management')
    slug = "projects"


class Sales(Dashboard):
    name = _('Sales')
    slug = "sales"


class TimeAndAttendance(Dashboard):
    name = _('Time and attendance')
    slug = "attendance"


class Warehouse(Dashboard):
    name = _('Warehouse')
    slug = "warehouse"
