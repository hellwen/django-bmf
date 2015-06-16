# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangobmf', '0005_added_unique_together'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportConf',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(verbose_name='Name', max_length=20)),
                ('renderer', models.CharField(verbose_name='Renderer', max_length=20)),
                ('mimetype', models.CharField(default='pdf', editable=False, verbose_name='Mimetype', max_length=20)),
                ('options', models.TextField(verbose_name='Options', help_text='Options for the renderer. Empty this field to get all available options with default values', blank=True)),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modified')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Report Configuration',
                'verbose_name_plural': 'Report Configurations',
                'get_latest_by': 'modified',
            },
        ),
    ]
