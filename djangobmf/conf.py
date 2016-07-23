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
        if not hasattr(djsettings, 'BMF_CONTRIB_ACCOUNT'):
            setattr(djsettings, 'BMF_CONTRIB_ACCOUNT', 'djangobmf_accounting.Account')
        return getattr(djsettings, 'BMF_CONTRIB_ACCOUNT')

    @property
    def CONTRIB_ADDRESS(self):  # noqa
        if not hasattr(djsettings, 'BMF_CONTRIB_ADDRESS'):
            setattr(djsettings, 'BMF_CONTRIB_ADDRESS', 'djangobmf_address.Address')
        return getattr(djsettings, 'BMF_CONTRIB_ADDRESS')

    @property
    def CONTRIB_CUSTOMER(self):  # noqa
        if not hasattr(djsettings, 'BMF_CONTRIB_CUSTOMER'):
            setattr(djsettings, 'BMF_CONTRIB_CUSTOMER', 'djangobmf_customer.Customer')
        return getattr(djsettings, 'BMF_CONTRIB_CUSTOMER')

    @property
    def CONTRIB_EMPLOYEE(self):  # noqa
        if not hasattr(djsettings, 'BMF_CONTRIB_EMPLOYEE'):
            setattr(djsettings, 'BMF_CONTRIB_EMPLOYEE', 'djangobmf_employee.Employee')
        return getattr(djsettings, 'BMF_CONTRIB_EMPLOYEE')

    @property
    def CONTRIB_GOAL(self):  # noqa
        if not hasattr(djsettings, 'BMF_CONTRIB_GOAL'):
            setattr(djsettings, 'BMF_CONTRIB_GOAL', 'djangobmf_task.Goal')
        return getattr(djsettings, 'BMF_CONTRIB_GOAL')

    @property
    def CONTRIB_INVOICE(self):  # noqa
        if not hasattr(djsettings, 'BMF_CONTRIB_INVOICE'):
            setattr(djsettings, 'BMF_CONTRIB_INVOICE', 'djangobmf_invoice.Invoice')
        return getattr(djsettings, 'BMF_CONTRIB_INVOICE')

    @property
    def CONTRIB_TAX(self):  # noqa
        if not hasattr(djsettings, 'BMF_CONTRIB_TAX'):
            setattr(djsettings, 'BMF_CONTRIB_TAX', 'djangobmf_taxing.Tax')
        return getattr(djsettings, 'BMF_CONTRIB_TAX')

    @property
    def CONTRIB_TASK(self):  # noqa
        if not hasattr(djsettings, 'BMF_CONTRIB_TASK'):
            setattr(djsettings, 'BMF_CONTRIB_TASK', 'djangobmf_task.Task')
        return getattr(djsettings, 'BMF_CONTRIB_TASK')

    @property
    def CONTRIB_TEAM(self):  # noqa
        if not hasattr(djsettings, 'BMF_CONTRIB_TEAM'):
            setattr(djsettings, 'BMF_CONTRIB_TEAM', 'djangobmf_team.Team')
        return getattr(djsettings, 'BMF_CONTRIB_TEAM')

    @property
    def CONTRIB_POSITION(self):  # noqa
        if not hasattr(djsettings, 'BMF_CONTRIB_POSITION'):
            setattr(djsettings, 'BMF_CONTRIB_POSITION', 'djangobmf_position.Position')
        return getattr(djsettings, 'BMF_CONTRIB_POSITION')

    @property
    def CONTRIB_PRODUCT(self):  # noqa
        if not hasattr(djsettings, 'BMF_CONTRIB_PRODUCT'):
            setattr(djsettings, 'BMF_CONTRIB_PRODUCT', 'djangobmf_product.Product')
        return getattr(djsettings, 'BMF_CONTRIB_PRODUCT')

    @property
    def CONTRIB_PROJECT(self):  # noqa
        if not hasattr(djsettings, 'BMF_CONTRIB_PROJECT'):
            setattr(djsettings, 'BMF_CONTRIB_PROJECT', 'djangobmf_project.Project')
        return getattr(djsettings, 'BMF_CONTRIB_PROJECT')

    @property
    def CONTRIB_QUOTATION(self):  # noqa
        if not hasattr(djsettings, 'BMF_CONTRIB_QUOTATION'):
            setattr(djsettings, 'BMF_CONTRIB_QUOTATION', 'djangobmf_quotation.Quotation')
        return getattr(djsettings, 'BMF_CONTRIB_QUOTATION')

    @property
    def CONTRIB_TIMESHEET(self):  # noqa
        if not hasattr(djsettings, 'BMF_CONTRIB_TIMESHEET'):
            setattr(djsettings, 'BMF_CONTRIB_TIMESHEET', 'djangobmf_timesheet.Timesheet')
        return getattr(djsettings, 'BMF_CONTRIB_TIMESHEET')

    @property
    def CONTRIB_TRANSACTION(self):  # noqa
        if not hasattr(djsettings, 'BMF_CONTRIB_TRANSACTION'):
            setattr(djsettings, 'BMF_CONTRIB_TRANSACTION', 'djangobmf_accounting.Transaction')
        return getattr(djsettings, 'BMF_CONTRIB_TRANSACTION')

    @property
    def CONTRIB_TRANSACTIONITEM(self):  # noqa
        if not hasattr(djsettings, 'BMF_CONTRIB_TRANSACTIONITEM'):
            setattr(djsettings, 'BMF_CONTRIB_TRANSACTIONITEM', 'djangobmf_accounting.TransactionItem')
        return getattr(djsettings, 'BMF_CONTRIB_TRANSACTIONITEM')

    @property
    def CONTRIB_WAREHOUSE(self):  # noqa
        if not hasattr(djsettings, 'BMF_CONTRIB_WAREHOUSE'):
            setattr(djsettings, 'BMF_CONTRIB_WAREHOUSE', 'djangobmf_location.Warehouse')
        return getattr(djsettings, 'BMF_CONTRIB_WAREHOUSE')

    @property
    def CONTRIB_LOCATION(self):  # noqa
        if not hasattr(djsettings, 'BMF_CONTRIB_LOCATION'):
            setattr(djsettings, 'BMF_CONTRIB_LOCATION', 'djangobmf_location.Location')
        return getattr(djsettings, 'BMF_CONTRIB_LOCATION')

    @property
    def CONTRIB_STOCK(self):  # noqa
        if not hasattr(djsettings, 'BMF_CONTRIB_STOCK'):
            setattr(djsettings, 'BMF_CONTRIB_STOCK', 'djangobmf_stock.Stock')
        return getattr(djsettings, 'BMF_CONTRIB_STOCK')

    @property
    def DEBUG(self):  # noqa
        return getattr(djsettings, 'DEBUG', False)

    @property
    def DEBUG_JS(self):  # noqa
        if self.DEBUG:
            return getattr(djsettings, 'BMF_DEBUG_JS', False)
        return False

    @property
    def DOCUMENT_STORAGE(self):  # noqa
        if not hasattr(djsettings, 'BMF_DOCUMENT_STORAGE'):
            setattr(djsettings, 'BMF_DOCUMENT_STORAGE', 'djangobmf.storage.Storage')
        return getattr(djsettings, 'BMF_DOCUMENT_STORAGE')

    @property
    def DOCUMENT_ROOT(self):  # noqa
        if not hasattr(djsettings, 'BMF_DOCUMENT_ROOT'):
            setattr(djsettings, 'BMF_DOCUMENT_ROOT', None)
        return getattr(djsettings, 'BMF_DOCUMENT_ROOT')

    @property
    def DOCUMENT_URL(self):  # noqa
        if not hasattr(djsettings, 'BMF_DOCUMENT_URL'):
            setattr(djsettings, 'BMF_DOCUMENT_URL', None)
        return getattr(djsettings, 'BMF_DOCUMENT_URL')

    @property
    def DOCUMENT_STATIC_PREFIX(self):  # noqa
        if not hasattr(djsettings, 'BMF_DOCUMENT_STATIC_PREFIX'):
            setattr(djsettings, 'BMF_DOCUMENT_STATIC_PREFIX', 'static')
        return getattr(djsettings, 'BMF_DOCUMENT_STATIC_PREFIX')

    @property
    def DOCUMENT_SENDTYPE(self):  # noqa
        if not hasattr(djsettings, 'BMF_DOCUMENT_SENDTYPE'):
            setattr(djsettings, 'BMF_DOCUMENT_SENDTYPE', None)
        return getattr(djsettings, 'BMF_DOCUMENT_SENDTYPE')

    @property
    def DOCUMENT_PERMISSIONS_FILE(self):  # noqa
        if not hasattr(djsettings, 'BMF_DOCUMENT_PERMISSIONS_FILE'):
            setattr(djsettings, 'BMF_DOCUMENT_PERMISSIONS_FILE', djsettings.FILE_UPLOAD_PERMISSIONS)
        return getattr(djsettings, 'BMF_DOCUMENT_PERMISSIONS_FILE')

    @property
    def DOCUMENT_PERMISSIONS_DIR(self):  # noqa
        if not hasattr(djsettings, 'BMF_DOCUMENT_PERMISSIONS_DIR'):
            setattr(djsettings, 'BMF_DOCUMENT_PERMISSIONS_DIR', djsettings.FILE_UPLOAD_DIRECTORY_PERMISSIONS)
        return getattr(djsettings, 'BMF_DOCUMENT_PERMISSIONS_DIR')

    @property
    def REPORTING(self):  # noqa
        return getattr(djsettings, 'BMF_REPORTING', {
            'pdf': ['djangobmf.models.PDFRenderer'],
        })

    @property
    def DEFAULT_CURRENCY(self):  # noqa
        return getattr(djsettings, 'BMF_DEFAULT_CURRENCY', 'EUR')

    @property
    def AUTH_EXPIRATION_DELTA(self):  # noqa
        return getattr(djsettings, 'BMF_AUTH_EXPIRATION_DELTA', 600)

    @property
    def AUTH_HEADER_PREFIX(self):  # noqa
        return getattr(djsettings, 'BMF_AUTH_HEADER_PREFIX', 'JWT')

    @property
    def AUTH_SECRET_KEY(self):  # noqa
        return getattr(djsettings, 'BMF_AUTH_SECRET_KEY', djsettings.SECRET_KEY)

    @property
    def AUTH_ISSUER(self):  # noqa
        return getattr(djsettings, 'BMF_AUTH_ISSUER', None)

    @property
    def AUTH_AUDIENCE(self):  # noqa
        return getattr(djsettings, 'BMF_AUTH_AUDIENCE', None)

    @property
    def AUTH_ALGORITHMS(self):  # noqa
        return getattr(djsettings, 'BMF_AUTH_ALGORITHMS', ['HS256'])

    def patch(self):
        """
        This function is used to update django.conf.settings in the testrunner.
        It updates django's settings with the default values from the bmf
        """
        for setting in [
            'CONTRIB_ACCOUNT',
            'CONTRIB_ADDRESS',
            'CONTRIB_CUSTOMER',
            'CONTRIB_EMPLOYEE',
            'CONTRIB_GOAL',
            'CONTRIB_INVOICE',
            'CONTRIB_TAX',
            'CONTRIB_TASK',
            'CONTRIB_TEAM',
            'CONTRIB_POSITION',
            'CONTRIB_PRODUCT',
            'CONTRIB_PROJECT',
            'CONTRIB_QUOTATION',
            'CONTRIB_TIMESHEET',
            'CONTRIB_TRANSACTION',
            'CONTRIB_TRANSACTIONITEM',
            'CONTRIB_WAREHOUSE',
            'CONTRIB_LOCATION',
            'CONTRIB_STOCK',
        ]:
            getattr(self, setting)


settings = Settings()
