# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import djangobmf.fields.country


class Migration(migrations.Migration):

    dependencies = [
        ('djangobmf_address', '0001_version_0_2_5'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='country',
            field=models.CharField(null=True, verbose_name='Country OLD', help_text='This field will be removed in an upcoming release of djangobmf', max_length=255, blank=True),
        ),
        migrations.RenameField(
            model_name='address',
            old_name='country',
            new_name='old_country',
        ),
        migrations.AddField(
            model_name='address',
            name='country',
            field=djangobmf.fields.country.CountryField(null=True),
        ),
    ]
