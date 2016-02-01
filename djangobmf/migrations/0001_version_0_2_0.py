# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djangobmf.utils.generate_filename
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
import djangobmf.storage


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
        migrations.swappable_dependency(settings.BMF_CONTRIB_PROJECT),
        migrations.swappable_dependency(settings.BMF_CONTRIB_CUSTOMER),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('topic', models.CharField(max_length=100, null=True, verbose_name='Topic', blank=True)),
                ('text', models.TextField(null=True, verbose_name='Text', blank=True)),
                ('action', models.PositiveSmallIntegerField(default=1, verbose_name='Action', null=True, editable=False, choices=[(1, 'Comment'), (2, 'Created'), (3, 'Updated'), (4, 'Workflow'), (5, 'File')])),
                ('template', models.CharField(verbose_name='Template', max_length=100, null=True, editable=False)),
                ('parent_id', models.PositiveIntegerField()),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modified')),
                ('parent_ct', models.ForeignKey(related_name='bmf_history_parent', to='contenttypes.ContentType')),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-modified',),
                'get_latest_by': 'modified',
                'verbose_name': 'History',
                'verbose_name_plural': 'History',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('app_label', models.CharField(verbose_name='Application', max_length=100, null=True, editable=False)),
                ('field_name', models.CharField(verbose_name='Fieldname', max_length=100, null=True, editable=False)),
                ('value', models.TextField(null=True, verbose_name='Value')),
            ],
            options={
                'default_permissions': ('change',),
                'verbose_name': 'Configuration',
                'verbose_name_plural': 'Configurations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Dashboard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, null=True, verbose_name='Name')),
                ('user', models.ForeignKey(related_name='+', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('name', 'id'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NumberCycle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name_template', models.CharField(max_length=64, null=True, verbose_name='Template', validators=[])),
                ('counter_start', models.PositiveIntegerField(default=1, null=True)),
                ('current_period', models.DateField(default=django.utils.timezone.now, null=True)),
                ('ct', models.OneToOneField(related_name='bmf_numbercycle', null=True, editable=False, to='contenttypes.ContentType')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('reporttype', models.CharField(max_length=20, verbose_name='Reporttype')),
                ('mimetype', models.CharField(default='pdf', verbose_name='Mimetype', max_length=20, editable=False)),
                ('options', models.TextField(help_text='Options for the renderer. Empty this field to get all available options with default values', verbose_name='Options', blank=True)),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modified')),
                ('contenttype', models.ForeignKey(related_name='bmf_report', blank=True, to='contenttypes.ContentType', help_text='Connect a Report to an BMF-Model', null=True)),
            ],
            options={
                'get_latest_by': 'modified',
                'verbose_name': 'Report',
                'verbose_name_plural': 'Reports',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('watch_id', models.PositiveIntegerField(null=True)),
                ('triggered', models.BooleanField(default=True, verbose_name='Triggered', db_index=True, editable=False)),
                ('unread', models.BooleanField(default=True, verbose_name='Unread', db_index=True, editable=False)),
                ('last_seen_object', models.PositiveIntegerField(null=True)),
                ('new_entry', models.BooleanField(default=False, db_index=True, verbose_name='New entry')),
                ('comment', models.BooleanField(default=False, db_index=True, verbose_name='Comment written')),
                ('file', models.BooleanField(default=False, db_index=True, verbose_name='File added')),
                ('changed', models.BooleanField(default=False, db_index=True, verbose_name='Object changed')),
                ('workflow', models.BooleanField(default=False, db_index=True, verbose_name='Workflowstate changed')),
                ('modified', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Modified', null=True, editable=False)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('watch_ct', models.ForeignKey(to='contenttypes.ContentType', null=True)),
            ],
            options={
                'ordering': ('-modified',),
                'default_permissions': (),
                'get_latest_by': 'modified',
                'verbose_name': 'Watched activity',
                'verbose_name_plural': 'Watched activities',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='notification',
            unique_together=set([('user', 'watch_ct', 'watch_id')]),
        ),
        migrations.CreateModel(
            name='Workspace',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(max_length=30)),
                ('url', models.CharField(max_length=255, editable=False, db_index=True)),
                ('public', models.BooleanField(default=True)),
                ('editable', models.BooleanField(default=True)),
                ('module', models.CharField(max_length=255, null=True, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('ct', models.ForeignKey(related_name='+', blank=True, to='contenttypes.ContentType', null=True)),
                ('parent', models.ForeignKey(related_name='children', blank=True, to='djangobmf.Workspace', null=True)),
            ],
            options={
                'verbose_name': 'Workspace',
                'verbose_name_plural': 'Workspace',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='workspace',
            unique_together=set([('parent', 'slug')]),
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(verbose_name='Name', max_length=120, null=True, editable=False, blank=True)),
                ('file', models.FileField(upload_to=djangobmf.utils.generate_filename.generate_filename, storage=djangobmf.storage.default_storage, verbose_name='File')),
                ('size', models.PositiveIntegerField(null=True, editable=False, blank=True)),
                ('is_static', models.BooleanField(default=False)),
                ('content_id', models.PositiveIntegerField(null=True, editable=False, blank=True)),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modified', null=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created', null=True)),
                ('content_type', models.ForeignKey(related_name='bmf_document', on_delete=django.db.models.deletion.SET_NULL, blank=True, editable=False, to='contenttypes.ContentType', null=True)),
                ('created_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.BMF_CONTRIB_CUSTOMER, null=True)),
                ('modified_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.BMF_CONTRIB_PROJECT, null=True)),
            ],
            options={
                'get_latest_by': 'modified',
                'verbose_name': 'Document',
                'verbose_name_plural': 'Documents',
            },
            bases=(models.Model,),
        ),
    ]
