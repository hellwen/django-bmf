# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djangobmf.fields
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.BMF_CONTRIB_PROJECT),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('modified', models.DateTimeField(null=True, auto_now=True, verbose_name='Modified')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created')),
                ('uuid', models.CharField(null=True, blank=True, verbose_name='UUID', max_length=100, db_index=True, editable=False)),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('balance_currency', djangobmf.fields.CurrencyField(max_length=4, editable=False)),
                ('balance', djangobmf.fields.MoneyField(blank=True, editable=False, default='0')),
                ('number', models.CharField(null=True, blank=True, unique=True, verbose_name='Number', max_length=30, db_index=True)),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('type', models.PositiveSmallIntegerField(choices=[(10, 'Income'), (20, 'Expense'), (30, 'Asset'), (40, 'Liability'), (50, 'Equity')], null=True, blank=True, verbose_name='Type')),
                ('read_only', models.BooleanField(default=False, verbose_name='Read-only')),
                ('comment', models.TextField(null=True, blank=True, verbose_name='Comment')),
                ('created_by', models.ForeignKey(null=True, blank=True, to=settings.AUTH_USER_MODEL, editable=False, on_delete=django.db.models.deletion.SET_NULL, related_name='+')),
                ('modified_by', models.ForeignKey(null=True, blank=True, to=settings.AUTH_USER_MODEL, editable=False, on_delete=django.db.models.deletion.SET_NULL, related_name='+')),
                ('parent', models.ForeignKey(null=True, blank=True, to=settings.BMF_CONTRIB_ACCOUNT, related_name='children')),
            ],
            options={
                'verbose_name_plural': 'Accounts',
                'verbose_name': 'Account',
                'ordering': ['number', 'name', 'type'],
                'abstract': False,
                'swappable': 'BMF_CONTRIB_ACCOUNT',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('modified', models.DateTimeField(null=True, auto_now=True, verbose_name='Modified')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created')),
                ('uuid', models.CharField(null=True, blank=True, verbose_name='UUID', max_length=100, db_index=True, editable=False)),
                ('state', djangobmf.fields.OLDWorkflowField(null=True, blank=True, db_index=True, editable=False, max_length=32)),
                ('text', models.CharField(max_length=255, verbose_name='Posting text')),
                ('draft', models.BooleanField(default=True, editable=False, verbose_name='Draft')),
                ('created_by', models.ForeignKey(null=True, blank=True, to=settings.AUTH_USER_MODEL, editable=False, on_delete=django.db.models.deletion.SET_NULL, related_name='+')),
                ('modified_by', models.ForeignKey(null=True, blank=True, to=settings.AUTH_USER_MODEL, editable=False, on_delete=django.db.models.deletion.SET_NULL, related_name='+')),
                ('project', models.ForeignKey(null=True, blank=True, to=settings.BMF_CONTRIB_PROJECT, on_delete=django.db.models.deletion.SET_NULL)),
            ],
            options={
                'verbose_name_plural': 'Transactions',
                'verbose_name': 'Transaction',
                'abstract': False,
                'swappable': 'BMF_CONTRIB_TRANSACTION',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TransactionItem',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('modified', models.DateTimeField(null=True, auto_now=True, verbose_name='Modified')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created')),
                ('uuid', models.CharField(null=True, blank=True, verbose_name='UUID', max_length=100, db_index=True, editable=False)),
                ('amount_currency', djangobmf.fields.CurrencyField(max_length=4, editable=False)),
                ('amount', djangobmf.fields.MoneyField(blank=True, default='0')),
                ('credit', models.BooleanField(choices=[(True, 'Credit'), (False, 'Debit')], default=True)),
                ('draft', models.BooleanField(default=True, editable=False, verbose_name='Draft')),
                ('account', models.ForeignKey(null=True, to=settings.BMF_CONTRIB_ACCOUNT, related_name='transactions', on_delete=django.db.models.deletion.PROTECT)),
                ('created_by', models.ForeignKey(null=True, blank=True, to=settings.AUTH_USER_MODEL, editable=False, on_delete=django.db.models.deletion.SET_NULL, related_name='+')),
                ('modified_by', models.ForeignKey(null=True, blank=True, to=settings.AUTH_USER_MODEL, editable=False, on_delete=django.db.models.deletion.SET_NULL, related_name='+')),
                ('transaction', models.ForeignKey(null=True, to=settings.BMF_CONTRIB_TRANSACTION, related_name='items')),
            ],
            options={
                'swappable': 'BMF_CONTRIB_TRANSACTIONITEM',
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
