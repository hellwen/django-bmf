#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from decimal import Decimal

from djangobmf.conf import settings
from djangobmf.models import BMFModel
from djangobmf.fields import CurrencyField
from djangobmf.fields import MoneyField

from .serializers import StockSerializer
from .serializers import StockProductSerializer


class StockManager(models.Manager):
    def get_queryset(self):
        related = ['employee']
        return super(StockManager, self).get_queryset() \
            .order_by('bill_no') \
            .select_related(*related)


class StockProductManager(models.Manager):
    def get_queryset(self):
        related = ['product']
        return super(StockProductManager, self).get_queryset() \
            .select_related(*related)


@python_2_unicode_compatible
class AbstractStock(BMFModel):
    """
    """

    bill_no = models.CharField(_("Bill no"), max_length=20, null=False, blank=False)
    description = models.TextField(_("Description"), null=True, blank=True)

    date = models.DateField(_("Date"), null=True, blank=False)
    employee = models.ForeignKey(
        settings.CONTRIB_EMPLOYEE, null=True, blank=True, on_delete=models.SET_NULL)

    stock_type = models.TextField(_("Stock type"), null=True, blank=True, editable=False)
    completed = models.BooleanField(_("Completed"), default=False, editable=False)

    objects = StockManager()

    net = models.FloatField(editable=False, blank=True, null=True)

    def get_products(self):
        if not hasattr(self, '_cache_products'):
            self._cache_products = self.stock_products.all().select_related('product')
        return self._cache_products

    def calc_net(self):
        val = Decimal(0)
        for item in self.get_products():
            val += item.calc_net()
        return val

    def bmf_clean(self):
        self.net = self.calc_net()

    class Meta(BMFModel.Meta):  # only needed for abstract models
        verbose_name = _('Stock')
        verbose_name_plural = _('Stocks')
        ordering = ['bill_no']
        abstract = True
        swappable = "BMF_CONTRIB_STOCK"

    class BMFMeta:
        observed_fields = ['net']
        serializer = StockSerializer
        has_files = True
        has_comments = True

    def __str__(self):
        return '#%s' % (self.bill_no)


class StockProduct(BMFModel):
    stock = models.ForeignKey(
        settings.CONTRIB_STOCK, null=True, blank=True,
        related_name="stock_products", on_delete=models.CASCADE,
    )

    product = models.ForeignKey(
        settings.CONTRIB_PRODUCT, null=True, blank=True,
        related_name="stockproduct_products", on_delete=models.PROTECT,
    )

    price_currency = CurrencyField()
    price_precision = models.PositiveSmallIntegerField(
        default=0, blank=True, null=True, editable=False,
    )
    price = MoneyField(_("Price"), blank=False)
    amount = models.IntegerField(_("Amount"), blank=False, default=0)

    location = models.ForeignKey(settings.CONTRIB_LOCATION, null=True, blank=True, on_delete=models.CASCADE)

    description = models.TextField(_("Description"), null=True, blank=True)

    objects = StockProductManager()

    def calc_all(self):
        if hasattr(self, '_calcs'):
            return self._calcs
        self._calcs = self.product.calc_tax(self.amount, self.price)
        return self._calcs

    def calc_net(self):
        return self.calc_all()[0]

    class BMFMeta:
        only_related = True
        serializer = StockProductSerializer


class Stock(AbstractStock):
    pass
