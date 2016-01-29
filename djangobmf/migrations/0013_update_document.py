# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.BMF_CONTRIB_CUSTOMER),
        migrations.swappable_dependency(settings.BMF_CONTRIB_PROJECT),
        ('djangobmf', '0012_delete_dashboard'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='customer_pk',
        ),
        migrations.RemoveField(
            model_name='document',
            name='project_pk',
        ),
        migrations.AddField(
            model_name='document',
            name='customer',
            field=models.ForeignKey(blank=True, related_name='documents', to=settings.BMF_CONTRIB_CUSTOMER, null=True, on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='document',
            name='description',
            field=models.TextField(blank=True, verbose_name='Description', null=True),
        ),
        migrations.AddField(
            model_name='document',
            name='mimetype',
            field=models.CharField(editable=False, max_length=50, verbose_name='Mimetype', null=True),
        ),
        migrations.AddField(
            model_name='document',
            name='project',
            field=models.ForeignKey(blank=True, related_name='documents', to=settings.BMF_CONTRIB_PROJECT, null=True, on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='document',
            name='sha1',
            field=models.CharField(editable=False, max_length=40, verbose_name='SHA1', null=True),
        ),
    ]
