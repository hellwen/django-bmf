# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('djangobmf', '0005_added_unique_together'),
    ]

    operations = [
        migrations.CreateModel(
            name='Renderer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(null=True, blank=True, verbose_name='Key', editable=False, max_length=255, db_index=True)),
                ('name', models.CharField(verbose_name='Name', max_length=20)),
                ('modified', models.DateTimeField(verbose_name='Modified', auto_now=True)),
            ],
            options={
                'verbose_name': 'Renderer',
                'verbose_name_plural': 'Renderer',
                'get_latest_by': 'modified',
                'abstract': False,
            },
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
            field=models.CharField(null=True, blank=True, verbose_name='Key', editable=False, max_length=255, db_index=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='contenttype',
            field=models.ForeignKey(null=True, blank=True, editable=False, related_name='bmf_report', to='contenttypes.ContentType', help_text='Connect a Report to an BMF-Model'),
        ),
        migrations.AddField(
            model_name='report',
            name='renderer',
            field=models.ForeignKey(null=True, blank=True, help_text='Connect a Report to an Renderer', on_delete=django.db.models.deletion.SET_NULL, related_name='reports', to='djangobmf.Renderer'),
        ),
    ]
