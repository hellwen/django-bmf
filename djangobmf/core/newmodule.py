#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.core.exceptions import ImproperlyConfigured
# from django.conf.urls import patterns
# from django.conf.urls import url
# from django.utils import six
# from django.utils.text import slugify

from djangobmf.core.workflow import Workflow

from djangobmf.permissions import ModulePermission
# from djangobmf.views import ModuleCloneView
from djangobmf.views import ModuleCreateView
from djangobmf.views import ModuleDeleteView
from djangobmf.views import ModuleDetail
# from djangobmf.views import ModuleFormAPI
# from djangobmf.views import ModuleReportView
from djangobmf.views import ModuleUpdateView
# from djangobmf.views import ModuleWorkflowView

import logging
logger = logging.getLogger(__name__)


class Module(object):
    """
    Under the Module Class the framework stores every informations
    needed to display and manage views and API's
    """
    workflow_class = None
    workflow_field_name = "state"

    detail = ModuleDetail
    create = ModuleCreateView
    delete = ModuleDeleteView
    update = ModuleUpdateView
    permissions = ModulePermission

    class_reports = {}
    object_reports = {}

    def __init__(self):
        # validation
        if not hasattr(self, 'model'):
            raise ImproperlyConfigured(
                'No model defined in %s.' % self.__class__
            )

        if self.workflow_class:
            if not issubclass(self.workflow_class, Workflow):
                raise ImproperlyConfigured(
                    "%s is not a Workflow in %s" % (
                        self.workflow_class.__name__,
                        self.__name__
                    )
                )
            self.workflow = self.workflow_class()

    def has_workflow(self):
        return bool(self.workflow_class)

    def has_class_reports(self):
        return bool(self.reports)

    def has_object_reports(self):
        return bool(self.object_reports)

    def serialize_class(self):
        return {}

    def serialize_object(self, obj):
        return {}

#   has_logging = False
#   has_comments = False
#   has_files = False

#   observed_fields = []
#   search_fields = []

#   detail = ModuleDetail
#   create = ModuleCreateView
#   delete = ModuleDeleteView
#   update = ModuleUpdateView
#   permissions = ModulePermission

#   clone = None
#   primary = True
#   report = None
#   default = False

#   detail_urlpatterns = None
#   api_urlpatterns = None

#   def __init__odl(self):
#       self.dashboards = []
#       self.manager = {}
#       self.detail_view = self.detail.as_view(model=self.model)

#       self.create_view = self.create
#       self.delete_view = self.delete
#       self.update_view = self.update

#   def list_reports(self):
#       if hasattr(self, 'listed_reports'):
#           return self.listed_reports
#       self.listed_reports = []

#       if isinstance(self.report, dict):
#           for label, view in six.iteritems(self.report):
#               key = slugify(label)
#               if isinstance(view, (list, tuple)) and len(view) == 2:
#                   # overwrite the label, and correct the view
#                   label = slugify(view[0])
#                   view = view[1]

#               if issubclass(view, ModuleReportView):
#                   self.listed_reports.append((key, label, view))

#       elif isinstance(self.report, bool):
#         self.listed_reports.append(('default', 'default', ModuleReportView))

#       elif self.report and issubclass(self.report, ModuleReportView):
#           self.listed_reports.append(('default', 'default', self.report))

#       # update model with all report views
#       self.model._bmfmeta.report_views = self.listed_reports

#       return self.listed_reports

#   def list_creates(self):
#       if hasattr(self, 'listed_creates'):
#           return self.listed_creates
#       self.listed_creates = []

#       if isinstance(self.create, dict):
#           for label, view in six.iteritems(self.create):
#               key = slugify(label)

#               if isinstance(view, (list, tuple)) and len(view) == 2:
#                 # overwrite the label, and use the correct the view function
#                 label = view[0]
#                 view = view[1]
#               self.listed_creates.append((key, label, view))

#       elif issubclass(self.create, ModuleCreateView):
#           self.listed_creates.append(('default', 'default', self.create))

#       # update model with all create views
#       self.model._bmfmeta.create_views = self.listed_creates

#       return self.listed_creates

#   def get_detail_urls(self):
#       # add custom url patterns
#       if self.detail_urlpatterns:
#           return self.detail_urlpatterns
#       return patterns('')

#   def get_api_urls(self):
#       reports = self.list_reports()
#       creates = self.list_creates()

#       urlpatterns = patterns(
#           '',
#           url(
#               r'^update/(?P<pk>[0-9]+)/$',
#               self.update.as_view(
#                   module=self,
#                   model=self.model
#               ),
#               name='update',
#           ),
#           url(
#               r'^update/(?P<pk>[0-9]+)/form/$',
#               ModuleFormAPI.as_view(
#                   module=self,
#                   model=self.model,
#                   form_view=self.update,
#               ),
#               name='update-form',
#           ),
#           url(
#               r'^delete/(?P<pk>[0-9]+)/$',
#               self.delete.as_view(
#                   module=self,
#                   model=self.model
#               ),
#               name='delete',
#           ),
#       )

#       if self.model._bmfmeta.can_clone:
#           urlpatterns += patterns(
#               '',
#               url(
#                   r'^clone/(?P<pk>[0-9]+)/$',
#                   self.clone.as_view(
#                       module=self,
#                       model=self.model
#                   ),
#                   name='clone',
#               ),
#               url(
#                   r'^clone/(?P<pk>[0-9]+)/form/$',
#                   ModuleFormAPI.as_view(
#                       module=self,
#                       model=self.model,
#                       form_view=self.clone,
#                   ),
#                   name='clone-form',
#               ),
#           )

#       for key, label, view in creates:
#           urlpatterns += patterns(
#               '',
#               url(
#                   r'^create/(?P<key>%s)/$' % key,
#                   view.as_view(
#                       module=self,
#                       model=self.model
#                   ),
#                   name='create',
#               ),
#               url(
#                   r'^create/(?P<key>%s)/form/$' % key,
#                   ModuleFormAPI.as_view(
#                       module=self,
#                       model=self.model,
#                       form_view=view,
#                   ),
#                   name='create-form',
#               ),
#           )

#       for key, label, view in reports:
#           urlpatterns += patterns(
#               '',
#               url(
#                   r'^report/(?P<pk>[0-9]+)/(?P<key>%s)/$' % key,
#                   view.as_view(
#                       module=self,
#                       model=self.model
#                   ),
#                   name='report',
#               ),
#           )

#       # workflow interactions
#       if self.model._bmfmeta.has_workflow:
#           urlpatterns += patterns(
#               '',
#               url(
#                   r'^workflow/(?P<pk>[0-9]+)/(?P<transition>\w+)/$',
#                   ModuleWorkflowView.as_view(
#                       module=self,
#                       model=self.model
#                   ),
#                   name='workflow',
#               ),
#           )

#       # add custom url patterns
#       if self.api_urlpatterns:
#           urlpatterns += self.api_urlpatterns

#       return urlpatterns
