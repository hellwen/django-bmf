# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.BMF_CONTRIB_CUSTOMER),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('modified', models.DateTimeField(verbose_name='Modified', null=True, auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created', null=True)),
                ('uuid', models.CharField(editable=False, max_length=100, null=True, db_index=True, verbose_name='UUID', blank=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active')),
                ('is_billing', models.BooleanField(default=True, verbose_name='Is billing')),
                ('is_shipping', models.BooleanField(default=True, verbose_name='Is shipping')),
                ('default_billing', models.BooleanField(default=False, verbose_name='Default billing')),
                ('default_shipping', models.BooleanField(default=False, verbose_name='Default shipping')),
                ('name', models.CharField(verbose_name='Name', max_length=255, null=True)),
                ('name2', models.CharField(null=True, verbose_name='Name2', max_length=255, blank=True)),
                ('street', models.CharField(verbose_name='Street', max_length=255, null=True)),
                ('zip', models.CharField(verbose_name='Zipcode', max_length=255, null=True)),
                ('city', models.CharField(verbose_name='City', max_length=255, null=True)),
                ('state', models.CharField(null=True, verbose_name='State', max_length=255, blank=True)),
                ('country', models.CharField(verbose_name='Country', max_length=255, null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, editable=False, null=True, related_name='+', blank=True, to=settings.AUTH_USER_MODEL)),
                ('customer', models.ForeignKey(related_name='customer_address', to=settings.BMF_CONTRIB_CUSTOMER)),
                ('modified_by', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, editable=False, null=True, related_name='+', blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Addresses',
                'abstract': False,
                'ordering': ['name'],
                'swappable': 'BMF_CONTRIB_ADDRESS',
                'verbose_name': 'Address',
            },
            bases=(models.Model,),
        ),
    ]
