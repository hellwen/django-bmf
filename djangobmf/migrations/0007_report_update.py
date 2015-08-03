# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangobmf', '0006_reportconf'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='contenttype',
        ),
        migrations.RemoveField(
            model_name='report',
            name='mimetype',
        ),
        migrations.RemoveField(
            model_name='report',
            name='options',
        ),
        migrations.RemoveField(
            model_name='report',
            name='reporttype',
        ),
        migrations.AddField(
            model_name='report',
            name='key',
            field=models.CharField(blank=True, null=True, max_length=255, verbose_name='Key'),
        ),
        migrations.AddField(
            model_name='report',
            name='renderer',
            field=models.CharField(blank=True, null=True, max_length=30, verbose_name='Renderer'),
        ),
    ]
