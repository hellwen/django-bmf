# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangobmf_accounting', '0003_transactionitem_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transactionitem',
            options={'ordering': ('-draft', '-date', 'credit', 'account__number', 'transaction__text')},
        ),
        migrations.AlterField(
            model_name='transactionitem',
            name='date',
            field=models.DateField(verbose_name='Date', null=True, blank=True),
        ),
    ]
