# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django

class Migration(migrations.Migration):
    dependencies = [
        ('djangobmf_project', '0001_initial'),
        migrations.swappable_dependency(settings.BMF_CONTRIB_CUSTOMER),
    ]
    operations = [
        migrations.AddField(
            model_name='project',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to=settings.BMF_CONTRIB_CUSTOMER, null=True, blank=True, related_name="bmf_projects"),
            preserve_default=True,
        ),
    ]
