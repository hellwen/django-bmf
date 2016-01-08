# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangobmf', '0009_notification_rename'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='watch_id',
            field=models.PositiveIntegerField(db_index=True, null=True),
        ),
    ]
