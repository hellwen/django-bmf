# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangobmf', '0008_report_contenttype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='key',
            field=models.CharField(max_length=255, null=True, verbose_name='Key', blank=True, unique=True),
        ),
    ]
