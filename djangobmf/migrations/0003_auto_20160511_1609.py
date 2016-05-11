# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import djangobmf.fields.file


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('djangobmf', '0002_remove_old_report'),
    ]

    operations = [
        migrations.CreateModel(
            name='PDFRenderer',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(verbose_name='Name', max_length=20)),
                ('size', models.CharField(verbose_name='Size', max_length=10, default='A4')),
                ('form', models.CharField(verbose_name='Size', max_length=10, default='A')),
                ('template_extends', models.CharField(null=True, verbose_name='Template Extends', blank=True, max_length=40)),
                ('letter', models.BooleanField(verbose_name='Letter', default=True)),
                ('letter_margin_top', models.PositiveIntegerField(verbose_name='Letter margin top', blank=True, null=True)),
                ('letter_margin_right', models.PositiveIntegerField(verbose_name='Letter margin right', default=40)),
                ('letter_margin_bottom', models.PositiveIntegerField(verbose_name='Letter margin bottom', default=10)),
                ('letter_margin_left', models.PositiveIntegerField(verbose_name='Letter margin left', blank=True, null=True)),
                ('page_margin_top', models.PositiveIntegerField(verbose_name='Page margin top', default=20)),
                ('page_margin_right', models.PositiveIntegerField(verbose_name='Page margin right', default=40)),
                ('page_margin_bottom', models.PositiveIntegerField(verbose_name='Page margin bottom', default=10)),
                ('page_margin_left', models.PositiveIntegerField(verbose_name='Page margin left', blank=True, null=True)),
                ('modified', models.DateTimeField(verbose_name='Modified', auto_now=True)),
                ('letter_background', djangobmf.fields.file.FileField(verbose_name='Letter background', blank=True, to='djangobmf.Document', related_name='+', null=True)),
                ('page_background', djangobmf.fields.file.FileField(verbose_name='Page background', blank=True, to='djangobmf.Document', related_name='+', null=True)),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
                'verbose_name': 'PDF Renderer',
                'verbose_name_plural': 'PDF Renderer',
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(verbose_name='Name', max_length=120)),
                ('slug', models.CharField(verbose_name='Slug', max_length=120)),
                ('renderer_pk', models.PositiveIntegerField(null=True, blank=True)),
                ('renderer_view', models.CharField(max_length=254)),
                ('has_object', models.NullBooleanField()),
                ('enabled', models.BooleanField(default=False)),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modified', null=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created', null=True)),
                ('contenttype', models.ForeignKey(null=True, blank=True, to='contenttypes.ContentType', related_name='bmf_report')),
                ('renderer_ct', models.ForeignKey(null=True, blank=True, to='contenttypes.ContentType', related_name='+')),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
                'verbose_name': 'Report',
                'verbose_name_plural': 'Reports',
            },
        ),
        migrations.AlterUniqueTogether(
            name='report',
            unique_together=set([('slug', 'contenttype')]),
        ),
    ]
