# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.BMF_CONTRIB_GOAL),
        ('djangobmf_timesheet', '0007_timesheet_billable'),
    ]

    operations = [
        migrations.AddField(
            model_name='timesheet',
            name='goal',
            field=models.ForeignKey(to=settings.BMF_CONTRIB_GOAL, null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True),
        ),
    ]
