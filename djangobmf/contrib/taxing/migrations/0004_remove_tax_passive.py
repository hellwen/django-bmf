# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangobmf_taxing', '0003_changed_verbose_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tax',
            name='passive',
        ),
    ]
