# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('djangobmf_accounting', '0005_nomptt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='parents',
            field=models.ManyToManyField(editable=False, to=settings.BMF_CONTRIB_ACCOUNT, related_name='children'),
            preserve_default=True,
        ),
    ]
