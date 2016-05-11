# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangobmf', '0001_squashed_0_2_9'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Renderer',
        ),
        migrations.DeleteModel(
            name='Report',
        ),
    ]
