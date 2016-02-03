# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djangobmf.fields.file


class Migration(migrations.Migration):

    dependencies = [
        ('djangobmf_invoice', '0005_new_workflowfield'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='invoice',
            field=djangobmf.fields.file.FileField(null=True, verbose_name='Invoice'),
        ),
    ]
