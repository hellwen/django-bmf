# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangobmf', '0011_added_numberrange'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Dashboard',
        ),
    ]
