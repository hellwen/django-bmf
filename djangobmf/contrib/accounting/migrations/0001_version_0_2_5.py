# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import djangobmf.fields
from django.conf import settings
import djangobmf.fields.workflow
import djangobmf.contrib.accounting.workflows


class Migration(migrations.Migration):

    replaces = [('djangobmf_accounting', '0001_version_0_2_0'), ('djangobmf_accounting', '0002_remove_uuid'), ('djangobmf_accounting', '0003_changed_verbose_name'), ('djangobmf_accounting', '0004_new_workflowfield'), ('djangobmf_accounting', '0005_nomptt'), ('djangobmf_accounting', '0006_symmetrical_false')]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        migrations.swappable_dependency(settings.BMF_CONTRIB_PROJECT),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('balance_currency', djangobmf.fields.CurrencyField(max_length=4, editable=False)),
                ('balance', djangobmf.fields.MoneyField(blank=True, editable=False, default=None)),
                ('number', models.CharField(verbose_name='Number', blank=True, max_length=30, null=True, db_index=True, unique=True)),
                ('name', models.CharField(verbose_name='Name', max_length=100)),
                ('type', models.PositiveSmallIntegerField(verbose_name='Type', blank=True, choices=[(10, 'Income'), (20, 'Expense'), (30, 'Asset'), (40, 'Liability'), (50, 'Equity')], null=True)),
                ('read_only', models.BooleanField(verbose_name='Read-only', default=False)),
                ('comment', models.TextField(verbose_name='Comment', blank=True, null=True)),
                ('modified', models.DateTimeField(verbose_name='Modified', auto_now=True, null=True)),
                ('created', models.DateTimeField(verbose_name='Created', auto_now_add=True, null=True)),
                ('created_by', models.ForeignKey(verbose_name='Created by', blank=True, related_name='+', null=True, to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.SET_NULL, editable=False)),
                ('modified_by', models.ForeignKey(verbose_name='Modified by', blank=True, related_name='+', null=True, to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.SET_NULL, editable=False)),
                ('parent', models.ForeignKey(blank=True, related_name='child', null=True, to=settings.BMF_CONTRIB_ACCOUNT)),
                ('parents', models.ManyToManyField(related_name='children', to=settings.BMF_CONTRIB_ACCOUNT, editable=False)),
            ],
            options={
                'verbose_name_plural': 'Accounts',
                'verbose_name': 'Account',
                'abstract': False,
                'ordering': ['number', 'name', 'type'],
                'swappable': 'BMF_CONTRIB_ACCOUNT',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('text', models.CharField(verbose_name='Posting text', max_length=255)),
                ('draft', models.BooleanField(verbose_name='Draft', editable=False, default=True)),
                ('state', djangobmf.fields.workflow.WorkflowField(max_length=32, workflow=djangobmf.contrib.accounting.workflows.TransactionWorkflow, db_index=True)),
                ('modified', models.DateTimeField(verbose_name='Modified', auto_now=True, null=True)),
                ('created', models.DateTimeField(verbose_name='Created', auto_now_add=True, null=True)),
                ('created_by', models.ForeignKey(verbose_name='Created by', blank=True, related_name='+', null=True, to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.SET_NULL, editable=False)),
                ('modified_by', models.ForeignKey(verbose_name='Modified by', blank=True, related_name='+', null=True, to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.SET_NULL, editable=False)),
                ('project', models.ForeignKey(blank=True, null=True, to=settings.BMF_CONTRIB_PROJECT, on_delete=django.db.models.deletion.SET_NULL)),
            ],
            options={
                'verbose_name': 'Transaction',
                'abstract': False,
                'verbose_name_plural': 'Transactions',
                'swappable': 'BMF_CONTRIB_TRANSACTION',
            },
        ),
        migrations.CreateModel(
            name='TransactionItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('amount_currency', djangobmf.fields.CurrencyField(max_length=4, editable=False)),
                ('amount', djangobmf.fields.MoneyField(blank=True, default=None)),
                ('credit', models.BooleanField(choices=[(True, 'Credit'), (False, 'Debit')], default=True)),
                ('draft', models.BooleanField(verbose_name='Draft', editable=False, default=True)),
                ('modified', models.DateTimeField(verbose_name='Modified', auto_now=True, null=True)),
                ('created', models.DateTimeField(verbose_name='Created', auto_now_add=True, null=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='transactions', to=settings.BMF_CONTRIB_ACCOUNT, null=True)),
                ('created_by', models.ForeignKey(verbose_name='Created by', blank=True, related_name='+', null=True, to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.SET_NULL, editable=False)),
                ('modified_by', models.ForeignKey(verbose_name='Modified by', blank=True, related_name='+', null=True, to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.SET_NULL, editable=False)),
                ('transaction', models.ForeignKey(related_name='items', to=settings.BMF_CONTRIB_TRANSACTION, null=True)),
            ],
            options={
                'swappable': 'BMF_CONTRIB_TRANSACTIONITEM',
                'abstract': False,
            },
        ),
    ]
