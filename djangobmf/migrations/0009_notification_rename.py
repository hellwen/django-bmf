# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangobmf', '0008_renderer_filefields'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='comment',
            new_name='comments',
        ),
        migrations.RenameField(
            model_name='notification',
            old_name='changed',
            new_name='detectchanges',
        ),
        migrations.RenameField(
            model_name='notification',
            old_name='file',
            new_name='files',
        ),
    ]
