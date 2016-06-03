#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.conf.urls import patterns
from django.conf.urls import url
from django.contrib.admin.sites import AlreadyRegistered
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from django.db.models import signals
from django.http import Http404
from django.utils import six
from django.utils.text import slugify

from rest_framework.reverse import reverse

from djangobmf.core.relationship import DocumentRelationship
from djangobmf.core.serializers.document import DocumentSerializer
from djangobmf.core.workflow import Workflow
from djangobmf.models import Document
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

    open_relation = None
    workflow_class = None
    workflow_field_name = "state"

    detail_view = ModuleDetail

    def __init__(self, bmfconfig):

        # validation
        if not hasattr(self, 'model'):
            raise ImproperlyConfigured(
                'No model defined in %s.' % self.__class__
            )

        self.bmfconfig = bmfconfig

        self._class_reports = {}
        self._object_reports = {}
        self._relations = []

        self.signals_setup()
        self.validate_workflow()

        # auto add document relationship
        if hasattr(self.model, '_bmfmeta') and self.model._bmfmeta.has_files:
            class FileDownload(DocumentRelationship):
                model_to = self.model
                serializer = DocumentSerializer
            self.add_relation(FileDownload, Document)

        # TODO: OLD OLD OLD
        self.create_view = self.create
        self.delete_view = self.delete
        self.update_view = self.update

    # --- misc ----------------------------------------------------------------

    def get_contenttype(self):  # pragma: no cover
        """
        returns the models contenttype
        """
        return ContentType.objects.get_for_model(self.model)

    # --- single views --------------------------------------------------------

    # TODO
    def get_update_view(self):
        """
        """
        pass

    # TODO
    def get_delete_view(self):
        """
        """
        pass

    def get_detail_view(self, request, *args, **kwargs):
        """
        generates a detail-view response
        """
        if hasattr(self, '_detail_view'):
            return self._detail_view(request, *args, **kwargs)
        self._detail_view = self.detail_view.as_view(
            module=self,
            model=self.model
        )
        return self._detail_view(request, *args, **kwargs)

    # --- serialization -------------------------------------------------------

    # TODO
    def serialize_class(self, request=None):
        """
        """
        return OrderedDict([
            ('app', self.model._meta.app_label),
            ('creates', self.get_create_views()),
            ('ct', self.get_contenttype().pk),
            ('model', self.model._meta.model_name),
            ('name', self.model._meta.verbose_name_plural),
            ('open_relation', self.open_relation),
            ('relations', self.get_relations(request)),
        ])

    # TODO
    def serialize_object(self, obj):
        """
        """
        return {}

    # --- workflow ------------------------------------------------------------

    # TODO
    def validate_workflow(self):
        """
        """
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
        """
        """
        return bool(self.workflow_class)

    # TODO
    def get_workflow_states(self, obj):
        """
        """
        pass

    # TODO
    def get_workflow_transitions(self, obj, state_name):
        """
        """
        pass

    # --- permissions ---------------------------------------------------------

    # TODO
    def get_permissions(self, obj):
        """
        """
        pass

    # --- Create views --------------------------------------------------------

    def has_create_views(self):
        """
        return True if the module has one or more create views
        """
        return getattr(self, '_has_create_views', False)

    # TODO
    def get_create_views(self):
        """
        """
        if self.bmfconfig:
            namespace_api = '%s:moduleapi_%s_%s' % (
                self.bmfconfig.label,
                self.model._meta.app_label,
                self.model._meta.model_name,
            )
            return [{
                'name': i[1],
                'url': reverse(namespace_api + ':create', kwargs={"key": i[0]}),
            } for i in self.list_creates()]
        return []

    # TODO
    def get_create_view(self, name):
        """
        """
        pass

    # TODO
    def add_create_view(self, name, view):
        """
        """
        pass
        self._has_create_views = True

    # --- Clone views ---------------------------------------------------------

    def has_clone_views(self):
        """
        return True if the module has one or more clone views
        """
        return getattr(self, '_has_clone_views', False)

    # TODO
    def get_clone_views(self):
        """
        """
        pass

    # TODO
    def get_clone_view(self, name):
        """
        """
        pass

    # TODO
    def add_clone_view(self, name, view):
        """
        """
        pass
        self._has_clone_views = True

    # --- Functions for both report types -------------------------------------

    def add_report(self, report):
        """
        """
        if not getattr(report, "renderer_class", None):
            raise ImproperlyConfigured(
                '%s needs a renderer_class attribute',
                report,
            )

        if report.has_object:
            return self.add_object_report(report)
        else:
            return self.add_class_report(report)

    # --- Class specific reports ----------------------------------------------

    # TODO
    def get_class_reports(self):
        """
        """
        pass

    # TODO
    def get_class_report(self, name):
        """
        """
        pass

    # TODO
    def add_class_report(self, report):
        """
        """
        self._class_reports[report.__name__] = {
            'class': report,
        }

    # --- Object specific reports ---------------------------------------------

    def get_object_reports(self):
        """
        Returns all available reports
        """
        qs = self.bmfconfig.get_model("Report").objects.filter(
            contenttype=self.get_contenttype(),
            enabled=True
        ).values('pk', 'name', 'slug', 'renderer_view')
        items = []
        for data in qs:
            cls = self._object_reports[data['renderer_view']]
            if data['renderer_view'] in self._object_reports:
                items.append({
                    'name': data['name'],
                    'slug': data['slug'],
                    'verbose_name': cls['class'].verbose_name,
                    'has_form': bool(cls['class'].form_class),
                })
            else:
                self.bmfconfig.get_model("Report").objects.filter(pk=data['pk']).update(enabled=False)
        return items

    def get_object_report(self, slug):
        """
        """
        obj = self.bmfconfig.get_model("Report").objects.get(
            contenttype=self.get_contenttype(),
            enabled=True,
            slug=slug,
        )
        if not obj.renderer:
            logger.error('No renderer defined')
            raise Http404

        if obj.renderer_view in self._object_reports:
            report = self._object_reports[obj.renderer_view]

            if not report["view"]:
                report["view"] = report["class"].as_view()

            return report['view'], obj.renderer
        else:
            raise Http404

    def add_object_report(self, report):
        """
        """
        name = report.__module__ + '.' + report.__name__
        self._object_reports[name] = {
            'class': report,
            'view': None,  # the view is added by get_object_report
        }

    # --- Class specific custom apis ------------------------------------------

    # TODO
    def get_class_apis(self):
        """
        """
        pass

    # TODO
    def get_class_api(self, name):
        """
        """
        pass

    # TODO
    def add_class_api(self, name, view):
        """
        """
        pass

    # --- Object specific custom apis -----------------------------------------

    # TODO
    def get_object_apis(self):
        """
        """
        pass

    # TODO
    def get_object_api(self, name):
        """
        """
        pass

    # TODO
    def add_object_api(self, name, view):
        """
        """
        pass

    # --- Object specific custom apis -----------------------------------------

    def has_relations(self):
        """
        return True if the module has one or more relations
        """
        return bool(self._relations)

    # TODO
    def get_relations(self, request):
        """
        """
        relations = []
        for relation in self._relations:
            perm = '%s.view_%s'
            info = (relation._model_to._meta.app_label, relation._model_to._meta.model_name)
            if not request.user.has_perms([perm % info]):
                continue

            data = OrderedDict([
                ('app_label', relation._model_from._meta.app_label),
                ('model_name', relation._model_from._meta.model_name),
                ('name', relation.name),
                ('slug', relation.slug),
                ('template', relation.template),
            ])
            relations.append(data)
        return relations

    # TODO
    def get_relation(self, name):
        """
        """
        pass

    # TODO
    def add_relation(self, cls, model_from):
        """
        """
        relation = cls()
        relation._model_from = model_from

        for obj in self._relations:
            if obj == relation:
                raise AlreadyRegistered(
                    'Can not register the relationship %s' % cls.__name__
                )
        self._relations.append(relation)

    # --- number ranges -------------------------------------------------------

    def has_numberranges(self):
        """
        """
        pass

    # TODO
    def get_numberranges(self):
        """
        """
        pass

    # TODO
    def get_numberrange(self, name):
        """
        """
        pass

    # TODO
    def add_numberrange(self, name, number_range):
        """
        """
        pass

    # --- Signals -------------------------------------------------------------

    def signals_setup(self):
        """
        Bind own signal methods to the djangos signals
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
        This function is called bevor a model instance is deleted
        """
        pass

    def signal_pre_init(self, *args, **kwargs):
        """
        This function is called bevor a model instance is initialized
        """
        pass

    def signal_pre_save(self, *args, **kwargs):
        """
        This function is called bevor a model instance is saved
        """
        pass

    def signal_post_delete(self, *args, **kwargs):
        """
        This function is called after a model instance is deleted
        """
        pass

    def signal_post_init(self, *args, **kwargs):
        """
        This function is called after a model instance is initialized
        """
        pass

    def signal_post_save(self, *args, **kwargs):
        """
        This function is called after a model instance is saved
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

        return self.listed_creates

    def get_detail_urls(self):
        # add custom url patterns
        if self.detail_urlpatterns:
            return self.detail_urlpatterns
        return patterns('')

    def get_api_urls(self):
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
