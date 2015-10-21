#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

"""
overwrites bmf settings from django's settings
"""

from django.conf import settings as djsettings


class Settings(object):
    """
    This objects holds all settings used from djangobmf. is presents
    the values as propertiers, which is neccecary for testing
    with variable settings
    """

    ACTIVITY_WORKFLOW = "glyphicon-random"
    ACTIVITY_COMMENT = "glyphicon-comment"
    ACTIVITY_UPDATED = "glyphicon-pencil"
    ACTIVITY_FILE = "glyphicon-paperclip"
    ACTIVITY_CREATED = "glyphicon-file"
    ACTIVITY_UNKNOWN = "glyphicon-question-sign"

    @property
    def APP_LABEL(self):  # noqa
        return getattr(djsettings, 'BMF_APP_LABEL', 'djangobmf')

    @property
    def USE_CELERY(self):  # noqa
        return getattr(djsettings, 'BMF_USE_CELERY', False)

    @property
    def CACHE_DEFAULT_CONNECTION(self):  # noqa
        return getattr(djsettings, 'BMF_CACHE_DEFAULT_CONNECTION', 'default')

    @property
    def CONTRIB_ACCOUNT(self):  # noqa
        return getattr(djsettings, 'BMF_CONTRIB_ACCOUNT', 'djangobmf_accounting.Account')

    @property
    def CONTRIB_ADDRESS(self):  # noqa
        return getattr(djsettings, 'BMF_CONTRIB_ADDRESS', 'djangobmf_address.Address')

    @property
    def CONTRIB_CUSTOMER(self):  # noqa
        return getattr(djsettings, 'BMF_CONTRIB_CUSTOMER', 'djangobmf_customer.Customer')

    @property
    def CONTRIB_EMPLOYEE(self):  # noqa
        return getattr(djsettings, 'BMF_CONTRIB_EMPLOYEE', 'djangobmf_employee.Employee')

    @property
    def CONTRIB_GOAL(self):  # noqa
        return getattr(djsettings, 'BMF_CONTRIB_GOAL', 'djangobmf_task.Goal')

    @property
    def CONTRIB_INVOICE(self):  # noqa
        return getattr(djsettings, 'BMF_CONTRIB_INVOICE', 'djangobmf_invoice.Invoice')

    @property
    def CONTRIB_TAX(self):  # noqa
        return getattr(djsettings, 'BMF_CONTRIB_TAX', 'djangobmf_taxing.Tax')

    @property
    def CONTRIB_TASK(self):  # noqa
        return getattr(djsettings, 'BMF_CONTRIB_TASK', 'djangobmf_task.Task')

    @property
    def CONTRIB_TEAM(self):  # noqa
        return getattr(djsettings, 'BMF_CONTRIB_TEAM', 'djangobmf_team.Team')

    @property
    def CONTRIB_POSITION(self):  # noqa
        return getattr(djsettings, 'BMF_CONTRIB_POSITION', 'djangobmf_position.Position')

    @property
    def CONTRIB_PRODUCT(self):  # noqa
        return getattr(djsettings, 'BMF_CONTRIB_PRODUCT', 'djangobmf_product.Product')

    @property
    def CONTRIB_PROJECT(self):  # noqa
        return getattr(djsettings, 'BMF_CONTRIB_PROJECT', 'djangobmf_project.Project')

    @property
    def CONTRIB_QUOTATION(self):  # noqa
        return getattr(djsettings, 'BMF_CONTRIB_QUOTATION', 'djangobmf_quotation.Quotation')

    @property
    def CONTRIB_TIMESHEET(self):  # noqa
        return getattr(djsettings, 'BMF_CONTRIB_TIMESHEET', 'djangobmf_timesheet.Timesheet')

    @property
    def CONTRIB_TRANSACTION(self):  # noqa
        return getattr(djsettings, 'BMF_CONTRIB_TRANSACTION', 'djangobmf_accounting.Transaction')

    @property
    def CONTRIB_TRANSACTIONITEM(self):  # noqa
        return getattr(djsettings, 'BMF_CONTRIB_TRANSACTIONITEM', 'djangobmf_accounting.TransactionItem')

    @property
    def REPORTING_SERVER(self):  # noqa
        return getattr(djsettings, 'BMF_REPORTING_SERVER', None)

    @property
    def DEFAULT_CURRENCY(self):  # noqa
        return getattr(djsettings, 'BMF_DEFAULT_CURRENCY', 'EUR')


settings = Settings()
