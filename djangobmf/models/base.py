#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import AppRegistryNotReady
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.db.models import signals
from django.db.models.base import ModelBase
from django.utils import six
from django.utils.translation import ugettext_lazy as _

from djangobmf.conf import settings as bmfsettings
from djangobmf.fields import WorkflowField
from djangobmf.workflow import Workflow
from djangobmf.core.filter_queryset import FilterQueryset

import types
import inspect
import logging
logger = logging.getLogger(__name__)


def add_signals(cls):
    # TODO add model from app config
    from djangobmf.models import Activity

    # TODO add model from app config
    from djangobmf.models import Notification

    # cleanup history and follows
    def post_delete(sender, instance, *args, **kwargs):
        Activity.objects.filter(
            parent_ct=ContentType.objects.get_for_model(sender),
            parent_id=instance.pk,
        ).delete()
        Notification.objects.filter(
            watch_ct=ContentType.objects.get_for_model(sender),
            watch_id=instance.pk,
        ).delete()
    signals.post_delete.connect(post_delete, sender=cls, weak=False)


# TODO:
# we should create a workflow-enabled model with a fixes workflow field (also in db) and skip the
# probably unneccesary options

# TODO:
# we also should move the "permission" to an bmfacl manager to access the queryset
# from related objects


class BMFOptions(object):
    """
    Options class for BMF models. Use this as an inner class called ``BMFMeta``::

      class MyModel(BMFModel):
        class BMFMeta:
          workflow = MyWorkflow
    """

    def __init__(self, cls, meta, options=None):

        # overwriteable =========================================================
        self.has_logging = True
        self.has_comments = False
        self.has_files = False
        self.can_clone = False

        # mark this model as only related, which means that it
        # won't get a detail view
        self.only_related = getattr(options, 'only_related', False)

        self.clean = False
        self.observed_fields = []
        self.search_fields = []
        self.number_cycle = None

        # add an workflow object to the class

        self.workflow_cls = getattr(
            options, 'workflow', None
        )

        if self.workflow_cls and not issubclass(self.workflow_cls, Workflow):
            raise ImproperlyConfigured(
                "%s is not a Workflow in %s" % (
                    self.workflow_cls.__name__,
                    cls.__name__
                )
            )

        # workflow_field_name
        self.workflow_field_name = getattr(
            options, 'workflow_field_name', 'state'
        )

        # shortcut to the instance workflow model
        # is filled via a post_init signal (see below)
        self.workflow = None

        # determines if the model has an workflow
        if self.workflow_cls and len(self.workflow_cls._transitions) > 0:
            self.has_workflow = True
        else:
            self.has_workflow = False

        # add an filter_queryset to the class

        filter_queryset = getattr(
            options, 'filter_queryset', None
        )

        if filter_queryset and not issubclass(filter_queryset, FilterQueryset):
            raise ImproperlyConfigured(
                "%s is not a FilterQueryset in %s" % (
                    filter_queryset.__name__,
                    cls.__name__
                )
            )
            self.filter_queryset = filter_queryset()
        else:
            self.filter_queryset = FilterQueryset()

        # workflow_field_name
        self.workflow_field_name = getattr(
            options, 'workflow_field_name', 'state'
        )

        # shortcut to the instance workflow model
        # is filled via a post_init signal (see below)
        self.workflow = None

        # determines if the model has an workflow
        if self.workflow_cls and len(self.workflow_cls._transitions) > 0:
            self.has_workflow = True
        else:
            self.has_workflow = False

        # protected =============================================================

        # used to detect changes
        self.changelog = {}

        # namespace detail
        self.namespace_detail = '%s:detail_%s_%s' % (bmfsettings.APP_LABEL, meta.app_label, meta.model_name)

        # namespace api
        self.namespace_api = '%s:moduleapi_%s_%s' % (bmfsettings.APP_LABEL, meta.app_label, meta.model_name)

        # is filled with create views (see core/module.py)
        self.create_views = []

        if options:
            options = inspect.getmembers(cls.BMFMeta)
        else:
            options = []

        # set options
        for key, value in options:
            # auto-set known options (no validation!)
            if key in [
                'has_logging',
                'has_comments',
                'has_files',
                'search_fields',
                'number_cycle',
                'clean',
                'can_clone',
            ]:
                setattr(self, key, value)

            # only observe valid fields
            if key == "observed_fields":
                for field in meta.local_fields:
                    if not field.rel and field.name in value \
                            and field.name not in ['created', 'modified', 'created_by', 'modified_by']:
                        self.observed_fields.append(field.name)

        if self.only_related:
            self.has_logging = False
            self.can_clone = False

        # determines if the model detects changes
        self.has_detectchanges = bool(self.observed_fields) and self.has_logging

        # determines if the model can be watched by a user
        self.has_watchfunction = self.has_workflow or self.has_detectchanges \
            or self.has_comments or self.has_files

        # determines if the model has an activity
        self.has_activity = self.has_logging or self.has_comments or self.has_files

        self.has_history = self.has_logging  # TODO OLD REMOVE ME


class BMFModelBase(ModelBase):
    """
    Metaclass for BMF models
    """

    def __new__(cls, name, bases, attrs):
        cls = super(BMFModelBase, cls).__new__(cls, name, bases, attrs)

        parents = [b for b in bases if isinstance(b, BMFModelBase)]
        if not parents:
            # If this is the ModelBase-Class itself - do nothing
            return cls
        if cls._meta.abstract:
            # Don't do anything on abstract models
            return cls

        # make bmf-attributes
        cls._bmfmeta = BMFOptions(cls, cls._meta, getattr(cls, 'BMFMeta', None))

        if type(cls._meta.permissions) is not tuple:
            cls._meta.permissions = tuple(cls._meta.permissions)

        # generate permissions
        if not cls._bmfmeta.only_related:
            cls._meta.permissions += (
                ('view_' + cls._meta.model_name, u'Can view %s' % cls.__name__),
            )
        if cls._bmfmeta.can_clone:
            cls._meta.permissions += (
                ('clone_' + cls._meta.model_name, u'Can clone %s' % cls.__name__),
            )
        if cls._bmfmeta.has_comments:
            cls._meta.permissions += (
                ('comment_' + cls._meta.model_name, u'Can comment on %s' % cls.__name__),
            )
        if cls._bmfmeta.has_files:
            cls._meta.permissions += (
                ('addfile_' + cls._meta.model_name, u'Can add files to %s' % cls.__name__),
            )

        # add field: workflow field
        if cls._bmfmeta.has_workflow:
            try:
                field = cls._meta.get_field(cls._bmfmeta.workflow_field_name)
                if not isinstance(field, WorkflowField):
                    raise ImproperlyConfigured(
                        '%s is not a WorkflowField in %s' % (
                            cls._bmfmeta.workflow_field_name,
                            cls.__name__
                        )
                    )

            except (models.FieldDoesNotExist, AppRegistryNotReady):
                field = WorkflowField(workflow=cls._bmfmeta.workflow_cls)
                field.contribute_to_class(cls, cls._bmfmeta.workflow_field_name)

        # add field: modified
        try:
            cls._meta.get_field('modified')
        except (models.FieldDoesNotExist, AppRegistryNotReady):
            field = models.DateTimeField(
                _("Modified"),
                auto_now=True,
                editable=False,
                null=True,
                blank=False,
            )
            field.contribute_to_class(cls, 'modified')

        # add field: created
        try:
            cls._meta.get_field('created')
        except (models.FieldDoesNotExist, AppRegistryNotReady):
            field = models.DateTimeField(
                _("Created"),
                auto_now_add=True,
                editable=False,
                null=True,
                blank=False,
            )
            field.contribute_to_class(cls, 'created')

        # add field: modified by
        try:
            cls._meta.get_field('modified_by')
        except (models.FieldDoesNotExist, AppRegistryNotReady):
            field = models.ForeignKey(
                getattr(settings, 'AUTH_USER_MODEL', 'auth.User'),
                verbose_name=_("Modified by"),
                null=True, blank=True, editable=False,
                related_name="+", on_delete=models.SET_NULL
            )
            field.contribute_to_class(cls, 'modified_by')

        # add field: created by
        try:
            cls._meta.get_field('created_by')
        except (models.FieldDoesNotExist, AppRegistryNotReady):
            field = models.ForeignKey(
                getattr(settings, 'AUTH_USER_MODEL', 'auth.User'),
                verbose_name=_("Created by"),
                null=True, blank=True, editable=False,
                related_name="+", on_delete=models.SET_NULL
            )
            field.contribute_to_class(cls, 'created_by')

        # TODO add model from app config
        try:
            cls._meta.get_field('djangobmf_activity')
        except (models.FieldDoesNotExist, AppRegistryNotReady):
            field = GenericRelation(
                "djangobmf.Activity",
                content_type_field='parent_ct',
                object_id_field='parent_id',
            )
            field.contribute_to_class(cls, 'djangobmf_activity')

        # TODO add model from app config
        try:
            cls._meta.get_field('djangobmf_notification')
        except (models.FieldDoesNotExist, AppRegistryNotReady):
            field = GenericRelation(
                "djangobmf.Notification",
                content_type_field='watch_ct',
                object_id_field='watch_id',
            )
            field.contribute_to_class(cls, 'djangobmf_notification')

        # instancemethod: bmfget_project
        def bmfget_project(self):
            """
            The result of this value is currently used by the document-management system
            to connect the file uploaded to this model with a project instance

            Default: None
            """
            return None

        setattr(cls, 'bmfget_project', bmfget_project)

        # instancemethod: bmfget_customer
        def bmfget_customer(self):
            """
            The result of this value is currently used by the document-management system
            to connect the file uploaded to this model with a customer instance

            Default: None
            """
            return None

        setattr(cls, 'bmfget_customer', bmfget_customer)

        # instancemethod: bmfmodule_detail
        def bmfmodule_detail(self):
            """
            A permalink to the default view of this model in the BMF-System
            """
            return ('%s:detail' % self._bmfmeta.namespace_detail, (), {"pk": self.pk})

        setattr(cls, 'bmfmodule_detail', models.permalink(bmfmodule_detail))

        # instancemethod: get_absolute_url
        def get_absolute_url(self):
            return self.bmfmodule_detail()

        setattr(cls, 'get_absolute_url', get_absolute_url)

        # classmethod: bmfmodule_list
        def bmfmodule_list(cls, manager="all"):
            """
            """
            return ('%s:get' % cls._bmfmeta.namespace_api, (), {"manager": manager})

        setattr(cls, 'bmfmodule_list', classmethod(models.permalink(bmfmodule_list)))

        if cls._bmfmeta.clean:
            if not hasattr(cls, 'bmf_clean') and not cls._meta.abstract:
                raise ImproperlyConfigured('%s has not a bmf_clean method' % (cls.__name__))

        # add history signals for this model
        add_signals(cls)

        if cls._bmfmeta.has_workflow:

            def post_init_workflow(sender, instance, *args, **kwargs):
                workflow = getattr(instance, instance._bmfmeta.workflow_field_name)
                workflow.set_django_object(instance)
                instance._bmfmeta.workflow = workflow

            signals.post_init.connect(post_init_workflow, sender=cls, weak=False)

        if cls._bmfmeta.observed_fields:

            def post_init_observed_fields(sender, instance, *args, **kwargs):
                if instance.pk:
                    for key in instance._bmfmeta.observed_fields:
                        instance._bmfmeta.changelog[key] = getattr(instance, key)

            signals.post_init.connect(post_init_observed_fields, sender=cls, weak=False)

#       # add signals from base-classes
#       if hasattr(cls,'pre_save'):
#           if isinstance(cls.pre_save, types.FunctionType):
#               signals.pre_save.connect(cls.pre_save, sender=cls, weak=False)

#       if hasattr(cls,'post_init'):
#           if isinstance(cls.post_init, types.FunctionType):
#               signals.post_init.connect(cls.post_init, sender=cls, weak=False)

        if hasattr(cls, 'post_save'):
            """
            @staticmethod
            def post_save(sender, instance, created, raw, *args, **kwargs):
              pass
            """
            if isinstance(cls.post_save, types.FunctionType):
                signals.post_save.connect(cls.post_save, sender=cls, weak=False)

        if hasattr(cls, 'post_delete'):
            """
            @staticmethod
            def post_delete(sender, instance, *args, **kwargs):
              pass
            """
            if isinstance(cls.post_delete, types.FunctionType):
                signals.post_delete.connect(cls.post_delete, sender=cls, weak=False)

        return cls


class BMFModel(six.with_metaclass(BMFModelBase, models.Model)):
    """
    Base class for BMF models.
    """
    class Meta:
        abstract = True
