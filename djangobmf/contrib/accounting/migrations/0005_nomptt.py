# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('djangobmf_accounting', '0004_new_workflowfield'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='level',
        ),
        migrations.RemoveField(
            model_name='account',
            name='lft',
        ),
        migrations.RemoveField(
            model_name='account',
            name='rght',
        ),
        migrations.RemoveField(
            model_name='account',
            name='tree_id',
        ),
        migrations.AddField(
            model_name='account',
            name='parents',
            field=models.ManyToManyField(related_name='parents_rel_+', to=settings.BMF_CONTRIB_ACCOUNT),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='parent',
            field=models.ForeignKey(null=True, related_name='child', to=settings.BMF_CONTRIB_ACCOUNT, blank=True),
            preserve_default=True,
        ),
    ]
