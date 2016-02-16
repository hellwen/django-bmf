# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djangobmf.fields.file


class Migration(migrations.Migration):

    dependencies = [
        ('djangobmf', '0007_update_renderer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='renderer',
            name='letter_background',
            field=djangobmf.fields.file.FileField(null=True, related_name='+', to='djangobmf.Document', blank=True, verbose_name='Letter background'),
        ),
        migrations.AlterField(
            model_name='renderer',
            name='page_background',
            field=djangobmf.fields.file.FileField(null=True, related_name='+', to='djangobmf.Document', blank=True, verbose_name='Page background'),
        ),
    ]
