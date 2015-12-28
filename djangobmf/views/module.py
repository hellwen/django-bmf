#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.contrib.admin.utils import NestedObjects
from django.contrib.auth import get_permission_codename
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
# from django.core.paginator import EmptyPage
# from django.core.paginator import PageNotAnInteger
# from django.core.paginator import Paginator
from django.core.urlresolvers import reverse as django_reverse
from django.db import router
from django.db.models import Q
from django.forms.fields import CharField
from django.forms.fields import FloatField
from django.forms.fields import DecimalField
from django.forms.models import ModelChoiceField
from django.http import Http404
from django.http import QueryDict
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import UpdateView
from django.views.generic.edit import BaseFormView
from django.views.generic.detail import SingleObjectMixin
from django.template.loader import get_template
from django.template.loader import select_template
from django.template import TemplateDoesNotExist
from django.utils.encoding import force_text
from django.utils.html import format_html
# from django.utils.timezone import make_aware
# from django.utils.timezone import get_current_timezone
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext

from .mixins import AjaxMixin
from .mixins import ModuleSearchMixin
from .mixins import ModuleBaseMixin
from .mixins import ModuleAjaxMixin
from .mixins import ModuleViewMixin
from .mixins import ModuleActivityMixin
from .mixins import ModuleFilesMixin
from .mixins import ModuleFormMixin
from .mixins import ReadOnlyMixin

from djangobmf.models import Report
from djangobmf.permissions import AjaxPermission
from djangobmf.permissions import ModuleViewPermission
from djangobmf.permissions import ModuleClonePermission
from djangobmf.permissions import ModuleCreatePermission
from djangobmf.permissions import ModuleDeletePermission
from djangobmf.permissions import ModuleUpdatePermission
from djangobmf.signals import activity_create
from djangobmf.signals import activity_update
# from djangobmf.utils.deprecation import RemovedInNextBMFVersionWarning

from rest_framework.reverse import reverse

import copy
# import datetime
import logging
import operator
import types
# import warnings

from functools import reduce
# from django_filters.views import FilterView

logger = logging.getLogger(__name__)


# --- detail, forms and api ---------------------------------------------------


class ModuleDetailView(ModuleBaseMixin, AjaxMixin, DetailView):
    """
    show the details of an entry
    """
    default_permission_classes = [ModuleViewPermission, AjaxPermission]
    context_object_name = 'object'
    template_name_suffix = '_bmfdetail'
    reports = []

    def get_ajax_context(self, **context):
        # shortcut
        meta = self.object._bmfmeta

        context.update({
            'views': {
                'update': reverse(
                    'djangobmf:moduleapi_%s_%s:update' % (
                        self.object._meta.app_label,
                        self.object._meta.model_name,
                    ), 
                    format=None,
                    request=self.request,
                    kwargs={'pk': self.object.pk},
                ),
                'delete': reverse(
                    'djangobmf:moduleapi_%s_%s:delete' % (
                        self.object._meta.app_label,
                        self.object._meta.model_name,
                    ), 
                    format=None,
                    request=self.request,
                    kwargs={'pk': self.object.pk},
                ),
                'comments': self.object._bmfmeta.has_comments,
                'activity': {
                    'enabled': self.object._bmfmeta.has_activity,
                    'url': reverse(
                        'djangobmf:api-activity',
                        format=None,
                        request=self.request,
                        kwargs={
                            'pk': self.object.pk,
                            'app': self.object._meta.app_label,
                            'model': self.object._meta.model_name,
                        },
                    ),
                },
            },
            'workflow': meta.workflow.serialize(self.request) if meta.workflow else None,
        })
        return context

    def get_template_names(self, related=True):
#       # self.update_notification()
#       if related and "open" in self.request.GET.keys() and \
#               self.request.GET["open"] in self.get_related_views().keys():
#           return self.get_related_views()[self.request.GET["open"]]["template"]

        return super(ModuleDetailView, self).get_template_names() \
            + ["djangobmf/api/detail-default.html"]


class ModuleReportView(ModuleViewMixin, DetailView):
    """
    render a report
    """
    permission_classes = [ModuleViewPermission]
    context_object_name = 'object'

    def get_template_names(self):
        return ["djangobmf/module_report.html"]

    def get(self, request, *args, **kwargs):
        response = super(ModuleReportView, self).get(request, *args, **kwargs)

        ct = ContentType.objects.get_for_model(self.get_object())
        try:
            report = Report.objects.get(contenttype=ct)
            return report.render(self.get_filename(), self.request, self.get_context_data())
        except Report.DoesNotExist:
            # return "no view configured" page
            return response

    def get_filename(self):
        return "report"


class ModuleCloneView(ModuleFormMixin, ModuleAjaxMixin, UpdateView):
    """
    clone a object
    """
    default_permission_classes = [ModuleClonePermission, AjaxPermission]
    context_object_name = 'object'
    template_name_suffix = '_bmfclone'
    fields = []

    def get_template_names(self):
        return super(ModuleCloneView, self).get_template_names() \
            + ["djangobmf/module_clone_default.html"]

    def clone_object(self, formdata, instance):
        pass

    def clone_related_objects(self, formdata, old_object, new_object):
        pass

    def form_object_save(self, form):
        self.object = form.save()

    def form_valid(self, form):
        # messages.success(self.request, 'Object cloned')
        old_object = copy.copy(self.object)
        self.clone_object(form.cleaned_data, form.instance)
        form.instance.pk = None
        if form.instance._bmfmeta.workflow:
            setattr(
                form.instance,
                form.instance._bmfmeta.workflow_field_name,
                form.instance._bmfmeta.workflow.default
            )
        form.instance.created_by = self.request.user
        form.instance.modified_by = self.request.user
        self.form_object_save(form)
        self.clone_related_objects(form.cleaned_data, old_object, self.object)
        activity_create.send(sender=self.object.__class__, instance=self.object)
        return self.render_valid_form({
            'object_pk': self.object.pk,
        #   'redirect': self.object.bmfmodule_detail(),
            'message': True,
            'reload': True,
        })


class ModuleUpdateView(ModuleFormMixin, ModuleAjaxMixin, ReadOnlyMixin, UpdateView):
    """
    """
    permission_classes = [ModuleUpdatePermission, AjaxPermission]
    context_object_name = 'object'
    template_name_suffix = '_bmfupdate'
    exclude = []

    def get_template_names(self):
        return super(ModuleUpdateView, self).get_template_names() \
            + ["djangobmf/module_update_default.html"]

    def form_valid(self, form):
        # messages.success(self.request, 'Object updated')
        form.instance.modified_by = self.request.user
        # TODO: get the values of all observed fields
        self.object = form.save()
        # TODO: compare the lists of observed fields
        # TODO: generate change signal
        # return dict([(field, getattr(self, field)) for field in self._bmfmeta.observed_fields])
        activity_update.send(sender=self.object.__class__, instance=self.object)
        if self.model._bmfmeta.only_related:
            return self.render_valid_form({
                'object_pk': self.object.pk,
                'message': True,
                'reload': True,
            })
        else:
            return self.render_valid_form({
                'object_pk': self.object.pk,
            #   'redirect': self.object.bmfmodule_detail(),
                'message': True,
                'reload': True,
            })


class ModuleCreateView(ModuleFormMixin, ModuleAjaxMixin, ReadOnlyMixin, CreateView):
    """
    create a new instance
    """
    permission_classes = [ModuleCreatePermission, AjaxPermission]
    context_object_name = 'object'
    template_name_suffix = '_bmfcreate'

    def get_template_names(self):
        return super(ModuleCreateView, self).get_template_names() \
            + ["djangobmf/module_create_default.html"]

    def form_object_save(self, form):
        self.object = form.save()
        activity_create.send(sender=self.object.__class__, instance=self.object)

    def form_valid(self, form):
        # messages.success(self.request, 'Object created')
        form.instance.modified_by = self.request.user
        form.instance.created_by = self.request.user
        self.form_object_save(form)

        return self.render_valid_form({
            'object_pk': self.object.pk,
            'message': True,
            'reload': True,
        })


class ModuleDeleteView(ModuleAjaxMixin, DeleteView):
    """
    delete an instance
    """
    permission_classes = [ModuleDeletePermission, AjaxPermission]
    context_object_name = 'object'
    template_name_suffix = '_bmfdelete'

    def get_template_names(self):
        return super(ModuleDeleteView, self).get_template_names() \
            + ["djangobmf/module_delete.html"]

    def get_deleted_objects(self):
        collector = NestedObjects(using=router.db_for_write(self.model))
        collector.collect([self.object])
        perms_needed = set()

        def format_callback(obj):

            p = '%s.%s' % (
                obj._meta.app_label,
                get_permission_codename('delete', obj._meta)
            )

            if not self.request.user.has_perm(p):
                perms_needed.add(obj._meta.verbose_name)

            registered = obj.__class__ in self.request.djangobmf_site.modules

            # only show bmf modules
            if not registered:
                return None

            return format_html(
                '{0}: {1}',
                obj._meta.verbose_name,
                obj
            )

        def format_protected_callback(obj):

        #   if obj.__class__ in self.request.djangobmf_site.modules and not obj._bmfmeta.only_related:
        #       return format_html(
        #           '{0}: <a href="{1}">{2}</a>',
        #           obj._meta.verbose_name,
        #           obj.bmfmodule_detail(),
        #           obj
        #       )
        #   else:
            return format_html(
                '{0}: {1}',
                obj._meta.verbose_name,
                obj
            )

        to_delete = collector.nested(format_callback)

        protected = [
            format_protected_callback(obj) for obj in collector.protected
        ]

        return to_delete, perms_needed, protected

    def get_success_url(self):
        # TODO redirect to active dashboard
        return django_reverse('djangobmf:dashboard', kwargs={
            'dashboard': None,
        })

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        if self.model._bmfmeta.only_related:
            return self.render_valid_form({
                'message': ugettext('Object deleted'),
                'reload': True,
            })
        else:
            return self.render_valid_form({
                'redirect': self.request.GET.get('redirect', success_url),
                'message': ugettext('Object deleted'),
            })

    def clean_list(self, lst):
        if not isinstance(lst, (list, tuple)):
            return lst
        else:
            return [x for x in map(self.clean_list, lst) if x]

    def get_context_data(self, **kwargs):
        context = super(ModuleDeleteView, self).get_context_data(**kwargs)

        to_delete, perms_needed, protected = self.get_deleted_objects()

        if perms_needed or protected:
            title = _("Cannot delete %(name)s") % {
                "name": force_text(self.model._meta.verbose_name)
            }
        else:
            title = _("Are you sure?")

        context['deleted_objects'] = self.clean_list(to_delete)
        context['object_name'] = self.model._meta.verbose_name
        context['perms_lacking'] = perms_needed
        context['protected'] = protected
        context['title'] = title

        return context


class ModuleWorkflowView(ModuleAjaxMixin, DetailView):
    """
    update the state of a workflow
    """
    permission_classes = [AjaxPermission]
    context_object_name = 'object'
    template_name_suffix = '_bmfworkflow'

    def get_template_names(self):
        return super(ModuleWorkflowView, self).get_template_names() \
            + ["djangobmf/module_workflow.html"]

    def get_permissions(self, perms):
        info = self.model._meta.app_label, self.model._meta.model_name
        perms.append('%s.change_%s' % info)
        perms.append('%s.view_%s' % info)
        return super(ModuleWorkflowView, self).get_permissions(perms)

    def get(self, request, transition, *args, **kwargs):
        self.object = self.get_object()

        try:
            success_url = self.object._bmfmeta.workflow.transition(transition, self.request.user)
        except ValidationError as e:
            return self.render_to_response({
                'error': e,
            })

        return self.render_valid_form({
            'message': True,
            'redirect': success_url,
            'reload': not bool(success_url),
        })


class ModuleFormAPI(ModuleFormMixin, ModuleAjaxMixin, ModuleSearchMixin, SingleObjectMixin, BaseFormView):
    """
    """
    permission_classes = [AjaxPermission]
    model = None
    queryset = None
    form_view = None

    def get_object(self, queryset=None):
        """
        Returns the object the view is displaying.
        """
        if hasattr(self, 'object'):
            return self.object
        # Use a custom queryset if provided; this is required for subclasses
        if queryset is None:
            queryset = self.get_queryset()

        # Next, try looking up by primary key.
        pk = self.kwargs.get('pk', None)
        if pk is None:
            return None
        try:
            obj = queryset.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") % {
                'verbose_name': queryset.model._meta.verbose_name
            })
        return obj

    def get_field(self, form, auto_id):
        """
        Get the field from the auto_id value of this form
        needed for ajax-interaction (search)
        """
        for field in form:
            if field.auto_id == auto_id:
                return field
        return None

    def get_all_fields(self, form):
        """
        Get all the fields in this form
        needed for ajax-interaction (changed value)
        """
        return [field for field in form]

    def get_changes(self, form):
        """
        needed for ajax calls. return fields, which changed between the validation
        """
        # do form validation
        valid = form.is_valid()

        # also do model clean's, which are usually done, if the model is valid
        try:
            form.instance.clean()
        except ValidationError:
            pass

        data = []
        for field in self.get_all_fields(form):
            # input-type fields
            val_instance = getattr(field.form.instance, field.name, None)

            if isinstance(field.field, (CharField, DecimalField, FloatField)):
                if not field.value() and val_instance:
                    data.append({'field': field.auto_id, 'value': val_instance})
                continue
            if isinstance(field.field, ModelChoiceField):
                try:  # inline formsets cause a attribute errors
                    if val_instance and field.value() != str(val_instance.pk):
                        data.append({'field': field.auto_id, 'value': val_instance.pk, 'name': str(val_instance)})
                except AttributeError:
                    pass
                continue
            logger.info("Formatting is missing for %s" % field.field.__class__)

        logger.debug("Form (%s) changes: %s" % (
            'valid' if valid else 'invalid',
            data
        ))

        return valid, data

    # Don't react on get requests
    def get(self, request, *args, **kwargs):
        raise Http404

    def post(self, request, *args, **kwargs):
        form_class = self.form_view(model=self.model, object=self.get_object()).get_form_class()
        data = self.request.POST['form'].encode('ASCII')
        form = form_class(
            prefix=self.get_prefix(),
            data=QueryDict(data),
            instance=self.get_object())

        if "search" in self.request.GET:
            # do form validation to fill form.instance with data
            valid = form.is_valid()

            field = self.get_field(form, self.request.POST['field'])
            if not field:
                logger.info("Field %s was not found" % self.request.POST['field'])
                raise Http404
            qs = field.field.queryset

            # use permissions from module
            try:
                module = self.request.djangobmf_site.get_module(qs.model)
                qs = module.permissions().filter_queryset(
                    qs,
                    self.request.user,
                )
            except KeyError:
                pass

            func = getattr(form.instance, 'get_%s_queryset' % field.name, None)
            if func:
                qs = func(qs)

            if self.request.POST['string']:
                for bit in self.normalize_query(self.request.POST['string']):
                    lookups = [self.construct_search(str(f)) for f in qs.model._bmfmeta.search_fields]
                    queries = [Q(**{l: bit}) for l in lookups]
                    qs = qs.filter(reduce(operator.or_, queries))
            data = []
            for item in qs:
                data.append({'pk': item.pk, 'value': str(item)})
            return self.render_to_json_response(data)

        if "changed" in self.request.GET:
            """
            validate one form and compare it to an new form created with the validated instance
            """
            valid, data = self.get_changes(form)

            return self.render_to_json_response(data)
        raise Http404

    def get_form_kwargs(self):
        kwargs = super(ModuleFormAPI, self).get_form_kwargs()
        kwargs.update({
            'instance': self.get_object(),
        })
        return kwargs
