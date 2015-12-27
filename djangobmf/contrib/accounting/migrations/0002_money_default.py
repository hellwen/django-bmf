# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import djangobmf.fields


class Migration(migrations.Migration):

    dependencies = [
        ('djangobmf_accounting', '0001_version_0_2_5'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='balance',
            field=djangobmf.fields.MoneyField(blank=True, editable=False, default=0),
        ),
    ]
