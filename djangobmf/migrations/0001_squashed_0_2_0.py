# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import djangobmf.numbering.validators
import djangobmf.utils.generate_filename
from django.conf import settings
import django.utils.timezone
import djangobmf.document.storage


class Migration(migrations.Migration):

    replaces = [('djangobmf', '0001_version_0_2_0'), ('djangobmf', '0008_activity_meta_options'), ('djangobmf', '0009_soft_dependency_for_projects_and_customer')]

    dependencies = [
        ('contenttypes', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('topic', models.CharField(blank=True, max_length=100, verbose_name='Topic', null=True)),
                ('text', models.TextField(blank=True, verbose_name='Text', null=True)),
                ('action', models.PositiveSmallIntegerField(choices=[(1, 'Comment'), (2, 'Created'), (3, 'Updated'), (4, 'Workflow'), (5, 'File')], verbose_name='Action', null=True, default=1, editable=False)),
                ('template', models.CharField(max_length=100, verbose_name='Template', null=True, editable=False)),
                ('parent_id', models.PositiveIntegerField()),
                ('modified', models.DateTimeField(verbose_name='Modified', auto_now=True)),
                ('parent_ct', models.ForeignKey(related_name='bmf_history_parent', to='contenttypes.ContentType')),
                ('user', models.ForeignKey(blank=True, null=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'History',
                'verbose_name': 'History',
                'get_latest_by': 'modified',
                'ordering': ('-modified',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('app_label', models.CharField(max_length=100, verbose_name='Application', null=True, editable=False)),
                ('field_name', models.CharField(max_length=100, verbose_name='Fieldname', null=True, editable=False)),
                ('value', models.TextField(verbose_name='Value', null=True)),
            ],
            options={
                'verbose_name_plural': 'Configurations',
                'verbose_name': 'Configuration',
                'default_permissions': ('change',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Dashboard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=100, verbose_name='Name', null=True)),
                ('user', models.ForeignKey(blank=True, null=True, to=settings.AUTH_USER_MODEL, related_name='+')),
            ],
            options={
                'ordering': ('name', 'id'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NumberCycle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name_template', models.CharField(validators=[djangobmf.numbering.validators.template_name_validator], max_length=64, verbose_name='Template', null=True)),
                ('counter_start', models.PositiveIntegerField(null=True, default=1)),
                ('current_period', models.DateField(null=True, default=django.utils.timezone.now)),
                ('ct', models.OneToOneField(related_name='bmf_numbercycle', null=True, to='contenttypes.ContentType', editable=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('reporttype', models.CharField(max_length=20, verbose_name='Reporttype')),
                ('mimetype', models.CharField(max_length=20, verbose_name='Mimetype', editable=False, default='pdf')),
                ('options', models.TextField(blank=True, help_text='Options for the renderer. Empty this field to get all available options with default values', verbose_name='Options')),
                ('modified', models.DateTimeField(verbose_name='Modified', auto_now=True)),
                ('contenttype', models.ForeignKey(blank=True, help_text='Connect a Report to an BMF-Model', null=True, to='contenttypes.ContentType', related_name='bmf_report')),
            ],
            options={
                'verbose_name_plural': 'Reports',
                'verbose_name': 'Report',
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('watch_id', models.PositiveIntegerField(null=True)),
                ('triggered', models.BooleanField(verbose_name='Triggered', editable=False, db_index=True, default=True)),
                ('unread', models.BooleanField(verbose_name='Unread', editable=False, db_index=True, default=True)),
                ('last_seen_object', models.PositiveIntegerField(null=True)),
                ('new_entry', models.BooleanField(verbose_name='New entry', default=False, db_index=True)),
                ('comment', models.BooleanField(verbose_name='Comment written', default=False, db_index=True)),
                ('file', models.BooleanField(verbose_name='File added', default=False, db_index=True)),
                ('changed', models.BooleanField(verbose_name='Object changed', default=False, db_index=True)),
                ('workflow', models.BooleanField(verbose_name='Workflowstate changed', default=False, db_index=True)),
                ('modified', models.DateTimeField(verbose_name='Modified', null=True, default=django.utils.timezone.now, editable=False)),
                ('user', models.ForeignKey(blank=True, null=True, to=settings.AUTH_USER_MODEL)),
                ('watch_ct', models.ForeignKey(to='contenttypes.ContentType', null=True)),
            ],
            options={
                'verbose_name_plural': 'Watched activities',
                'verbose_name': 'Watched activity',
                'default_permissions': (),
                'ordering': ('-modified',),
                'get_latest_by': 'modified',
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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('slug', models.SlugField(max_length=30)),
                ('url', models.CharField(max_length=255, editable=False, db_index=True)),
                ('public', models.BooleanField(default=True)),
                ('editable', models.BooleanField(default=True)),
                ('module', models.CharField(blank=True, max_length=255, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('ct', models.ForeignKey(blank=True, null=True, to='contenttypes.ContentType', related_name='+')),
                ('parent', models.ForeignKey(blank=True, null=True, to='djangobmf.Workspace', related_name='children')),
            ],
            options={
                'verbose_name_plural': 'Workspace',
                'verbose_name': 'Workspace',
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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(blank=True, max_length=120, verbose_name='Name', null=True, editable=False)),
                ('file', models.FileField(upload_to=djangobmf.utils.generate_filename.generate_filename, storage=djangobmf.document.storage.BMFStorage(), verbose_name='File')),
                ('size', models.PositiveIntegerField(blank=True, null=True, editable=False)),
                ('is_static', models.BooleanField(default=False)),
                ('content_id', models.PositiveIntegerField(blank=True, null=True, editable=False)),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modified', null=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created', null=True)),
                ('content_type', models.ForeignKey(blank=True, null=True, to='contenttypes.ContentType', related_name='bmf_document', editable=False, on_delete=django.db.models.deletion.SET_NULL)),
                ('created_by', models.ForeignKey(blank=True, null=True, to=settings.AUTH_USER_MODEL, related_name='+', editable=False, on_delete=django.db.models.deletion.SET_NULL)),
                ('modified_by', models.ForeignKey(blank=True, null=True, to=settings.AUTH_USER_MODEL, related_name='+', editable=False, on_delete=django.db.models.deletion.SET_NULL)),
                ('customer_pk', models.PositiveIntegerField(blank=True, null=True, db_index=True, editable=False)),
                ('project_pk', models.PositiveIntegerField(blank=True, null=True, db_index=True, editable=False)),
            ],
            options={
                'verbose_name_plural': 'Documents',
                'verbose_name': 'Document',
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='activity',
            options={'verbose_name_plural': 'Activity', 'verbose_name': 'Activity', 'get_latest_by': 'modified', 'ordering': ('-modified',)},
        ),
    ]
