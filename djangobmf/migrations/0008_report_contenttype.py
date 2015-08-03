# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('djangobmf', '0007_report_update'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='contenttype',
            field=models.ForeignKey(blank=True, null=True, related_name='bmf_report', to='contenttypes.ContentType', help_text='Connect a Report to an BMF-Model'),
        ),
    ]
