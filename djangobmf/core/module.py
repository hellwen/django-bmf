#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from django.db.models import signals

from django.conf.urls import patterns
from django.conf.urls import url
from django.utils import six
from django.utils.text import slugify

from djangobmf.core.workflow import Workflow

from djangobmf.permissions import ModulePermission
from djangobmf.views import ModuleCreateView
from djangobmf.views import ModuleDeleteView
from djangobmf.views import ModuleDetail
from djangobmf.views import ModuleFormAPI
from djangobmf.views import ModuleUpdateView
from djangobmf.views import ModuleWorkflowView

from collections import OrderedDict

import logging
logger = logging.getLogger(__name__)


class Module(object):
    """
    Under the ``Module`-class the framework stores every informations
    needed to display and manage views and API's. It also provides
    many functions used in the whole framework.
    """

    workflow_class = None
    workflow_field_name = "state"

    def __init__(self, config):
        # validation
        if not hasattr(self, 'model'):
            raise ImproperlyConfigured(
                'No model defined in %s.' % self.__class__
            )

        self.config = config

        self.signals_setup()
        self.validate_workflow()

        # TODO: OLD OLD OLD
        self.create_view = self.create
        self.delete_view = self.delete
        self.update_view = self.update
        self.detail_view = self.detail.as_view(model=self.model)

    # --- misc ----------------------------------------------------------------

    def get_contenttype(self):
        """
        returns the models contenttype
        """
        return ContentType.objects.get_for_model(self.model)

    # --- single views --------------------------------------------------------

    def get_update_view(self):
        pass

    def get_delete_view(self):
        pass

    def get_detail_view(self):
        pass

    # --- serialization -------------------------------------------------------

    def serialize_class(self):
        return OrderedDict([
            ('ct', self.get_contenttype().pk),
            ('app', self.model._meta.app_label),
            ('model', self.model._meta.model_name),
            ('name', self.model._meta.verbose_name_plural),
            ('creates', self.get_create_views()),
            ('relations', self.get_relations()),
        ])

    def serialize_object(self, obj):
        return {}

    # --- workflow ------------------------------------------------------------

    def validate_workflow(self):
        if self.workflow_class:
            if not issubclass(self.workflow_class, Workflow):
                raise ImproperlyConfigured(
                    "%s is not a Workflow in %s" % (
                        self.workflow_class.__name__,
                        self.__name__
                    )
                )
            # self.workflow = self.workflow_class()

    def has_workflow(self):
        return bool(self.workflow_class)

    def get_workflow_states(self, obj):
        pass

    def get_workflow_transitions(self, obj, state_name):
        pass

    # --- permissions ---------------------------------------------------------

    def get_permissions(self, obj):
        pass

    # --- Create views --------------------------------------------------------

    def has_create_views(self):
        """
        return True if the module has one or more create views
        """
        return getattr(self, '_has_create_views', False)

    def get_create_views(self):
        pass
        # {
        #     "name": i[1],
        #     "url": reverse(model._bmfmeta.namespace_api + ':create', kwargs={
        #         "key": i[0],
        #     }),
        # } for i in model._bmfmeta.create_views

    def get_create_view(self, name):
        pass

    def add_create_view(self, name, view):
        pass
        self._has_create_views = True

    # --- Clone views ---------------------------------------------------------

    def has_clone_views(self):
        """
        return True if the module has one or more clone views
        """
        return getattr(self, '_has_clone_views', False)

    def get_clone_views(self):
        pass

    def get_clone_view(self, name):
        pass

    def add_clone_view(self, name, view):
        pass
        self._has_clone_views = True

    # --- Class specific reports ----------------------------------------------

    def has_class_reports(self):
        """
        return True if the module has one or more class reports
        """
        return getattr(self, '_has_class_reports', False)

    def get_class_reports(self):
        pass

    def get_class_report(self, name):
        pass

    def add_class_report(self, name, report):
        pass

    # --- Object specific reports ---------------------------------------------

    def has_object_reports(self):
        """
        return True if the module has one or more object reports
        """
        return getattr(self, '_has_object_reports', False)

    def get_object_reports(self):
        pass

    def get_object_report(self, name):
        pass

    def add_object_report(self, name, report):
        pass

    # --- Class specific custom apis ------------------------------------------

    def has_class_apis(self):
        """
        return True if the module has one or more class apis
        """
        return getattr(self, '_has_class_apis', False)

    def get_class_apis(self):
        pass

    def get_class_api(self, name):
        pass

    def add_class_api(self, name, view):
        pass

    # --- Object specific custom apis -----------------------------------------

    def has_object_apis(self):
        """
        return True if the module has one or more object apis
        """
        return getattr(self, '_has_object_apis', False)

    def get_object_apis(self):
        pass

    def get_object_api(self, name):
        pass

    def add_object_api(self, name, view):
        pass

    # --- Object specific custom apis -----------------------------------------

    def has_relations(self):
        """
        return True if the module has one or more relations
        """
        return getattr(self, '_has_relations', False)

    def get_relations(self):
        pass
        # ('relations', relations.get(ct, [])),

    def get_relation(self, name):
        pass

    def add_relation(self, name, relation):
        pass

    # --- number ranges -------------------------------------------------------

    def has_numberranges(self):
        pass

    def get_numberranges(self):
        pass

    def get_numberrange(self, name):
        pass

    def add_numberrange(self, name, number_range):
        pass

    # --- Signals -------------------------------------------------------------

    def signals_setup(self):
        """
        bind own signal methods to the djangos signals
        """
        logger.debug("Setup signals for %s", self.__class__.__name__)
        signals.pre_delete.connect(self.signal_pre_delete, sender=self.model)
        signals.pre_init.connect(self.signal_pre_init, sender=self.model)
        signals.pre_save.connect(self.signal_pre_save, sender=self.model)
        signals.post_delete.connect(self.signal_post_delete, sender=self.model)
        signals.post_init.connect(self.signal_post_init, sender=self.model)
        signals.post_save.connect(self.signal_post_save, sender=self.model)

    def signal_pre_delete(self, *args, **kwargs):
        """
        this function is called bevor a model instance is deleted
        """
        pass

    def signal_pre_init(self, *args, **kwargs):
        """
        this function is called bevor a model instance is initialized
        """
        pass

    def signal_pre_save(self, *args, **kwargs):
        """
        this function is called bevor a model instance is saved
        """
        pass

    def signal_post_delete(self, *args, **kwargs):
        """
        this function is called after a model instance is deleted
        """
        pass

    def signal_post_init(self, *args, **kwargs):
        """
        this function is called after a model instance is initialized
        """
        pass

    def signal_post_save(self, *args, **kwargs):
        """
        this function is called after a model instance is saved
        """
        pass

    # TODO: OLD OLD OLD OLD OLD OLD OLD OLD OLD OLD OLD OLD OLD OLD OLD OLD OLD

    detail = ModuleDetail
    create = ModuleCreateView
    delete = ModuleDeleteView
    update = ModuleUpdateView
    permissions = ModulePermission

    detail_urlpatterns = None
    api_urlpatterns = None

    def list_reports(self):
        return []

    def list_creates(self):
        if hasattr(self, 'listed_creates'):
            return self.listed_creates
        self.listed_creates = []

        if isinstance(self.create, dict):
            for label, view in six.iteritems(self.create):
                key = slugify(label)

                if isinstance(view, (list, tuple)) and len(view) == 2:
                    # overwrite the label, and use the correct the view function
                    label = view[0]
                    view = view[1]
                self.listed_creates.append((key, label, view))

        elif issubclass(self.create, ModuleCreateView):
            self.listed_creates.append(('default', 'default', self.create))

        # update model with all create views
        self.model._bmfmeta.create_views = self.listed_creates

        return self.listed_creates

    def get_detail_urls(self):
        # add custom url patterns
        if self.detail_urlpatterns:
            return self.detail_urlpatterns
        return patterns('')

    def get_api_urls(self):
        reports = self.list_reports()
        creates = self.list_creates()

        urlpatterns = patterns(
            '',
            url(
                r'^update/(?P<pk>[0-9]+)/$',
                self.update.as_view(
                    module=self,
                    model=self.model
                ),
                name='update',
            ),
            url(
                r'^update/(?P<pk>[0-9]+)/form/$',
                ModuleFormAPI.as_view(
                    module=self,
                    model=self.model,
                    form_view=self.update,
                ),
                name='update-form',
            ),
            url(
                r'^delete/(?P<pk>[0-9]+)/$',
                self.delete.as_view(
                    module=self,
                    model=self.model
                ),
                name='delete',
            ),
        )

        if self.model._bmfmeta.can_clone:
            urlpatterns += patterns(
                '',
                url(
                    r'^clone/(?P<pk>[0-9]+)/$',
                    self.clone.as_view(
                        module=self,
                        model=self.model
                    ),
                    name='clone',
                ),
                url(
                    r'^clone/(?P<pk>[0-9]+)/form/$',
                    ModuleFormAPI.as_view(
                        module=self,
                        model=self.model,
                        form_view=self.clone,
                    ),
                    name='clone-form',
                ),
            )

        for key, label, view in creates:
            urlpatterns += patterns(
                '',
                url(
                    r'^create/(?P<key>%s)/$' % key,
                    view.as_view(
                        module=self,
                        model=self.model
                    ),
                    name='create',
                ),
                url(
                    r'^create/(?P<key>%s)/form/$' % key,
                    ModuleFormAPI.as_view(
                        module=self,
                        model=self.model,
                        form_view=view,
                    ),
                    name='create-form',
                ),
            )

        for key, label, view in reports:
            urlpatterns += patterns(
                '',
                url(
                    r'^report/(?P<pk>[0-9]+)/(?P<key>%s)/$' % key,
                    view.as_view(
                        module=self,
                        model=self.model
                    ),
                    name='report',
                ),
            )

        # workflow interactions
        if self.model._bmfmeta.has_workflow:
            urlpatterns += patterns(
                '',
                url(
                    r'^workflow/(?P<pk>[0-9]+)/(?P<transition>\w+)/$',
                    ModuleWorkflowView.as_view(
                        module=self,
                        model=self.model
                    ),
                    name='workflow',
                ),
            )

        # add custom url patterns
        if self.api_urlpatterns:
            urlpatterns += self.api_urlpatterns

        return urlpatterns

#   has_logging = False
#   has_comments = False
#   has_files = False

#   observed_fields = []
#   search_fields = []

#   clone = None
#   primary = True
#   report = None

#   def __init__odl(self):
#       self.dashboards = []
#       self.manager = {}
