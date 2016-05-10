# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import djangobmf.fields.file


class Migration(migrations.Migration):

    dependencies = [
        ('djangobmf', '0001_squashed_0_2_9'),
    ]

    operations = [
        migrations.CreateModel(
            name='PDFRenderer',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=20, verbose_name='Name')),
                ('size', models.CharField(max_length=10, default='A4', verbose_name='Size')),
                ('form', models.CharField(max_length=10, default='A', verbose_name='Size')),
                ('template_extends', models.CharField(max_length=40, verbose_name='Template Extends', blank=True, null=True)),
                ('letter', models.BooleanField(default=True, verbose_name='Letter')),
                ('letter_margin_top', models.PositiveIntegerField(verbose_name='Letter margin top', blank=True, null=True)),
                ('letter_margin_right', models.PositiveIntegerField(default=40, verbose_name='Letter margin right')),
                ('letter_margin_bottom', models.PositiveIntegerField(default=10, verbose_name='Letter margin bottom')),
                ('letter_margin_left', models.PositiveIntegerField(verbose_name='Letter margin left', blank=True, null=True)),
                ('page_margin_top', models.PositiveIntegerField(default=20, verbose_name='Page margin top')),
                ('page_margin_right', models.PositiveIntegerField(default=40, verbose_name='Page margin right')),
                ('page_margin_bottom', models.PositiveIntegerField(default=10, verbose_name='Page margin bottom')),
                ('page_margin_left', models.PositiveIntegerField(verbose_name='Page margin left', blank=True, null=True)),
                ('modified', models.DateTimeField(verbose_name='Modified', auto_now=True)),
                ('letter_background', djangobmf.fields.file.FileField(related_name='+', verbose_name='Letter background', blank=True, to='djangobmf.Document', null=True)),
                ('page_background', djangobmf.fields.file.FileField(related_name='+', verbose_name='Page background', blank=True, to='djangobmf.Document', null=True)),
            ],
            options={
                'abstract': False,
                'verbose_name_plural': 'PDF Renderer',
                'get_latest_by': 'modified',
                'verbose_name': 'PDF Renderer',
            },
        ),
        migrations.RemoveField(
            model_name='renderer',
            name='letter_background',
        ),
        migrations.RemoveField(
            model_name='renderer',
            name='page_background',
        ),
        migrations.RemoveField(
            model_name='report',
            name='contenttype',
        ),
        migrations.RemoveField(
            model_name='report',
            name='renderer',
        ),
        migrations.DeleteModel(
            name='Renderer',
        ),
        migrations.DeleteModel(
            name='Report',
        ),
    ]
