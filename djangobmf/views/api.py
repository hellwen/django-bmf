#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.apps import apps
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from django.template.loader import get_template
from django.template.loader import select_template

from djangobmf.filters import ViewFilterBackend
from djangobmf.filters import RangeFilterBackend
from djangobmf.filters import RelatedFilterBackend
from djangobmf.pagination import ModulePagination
from djangobmf.views.mixins import BaseMixin

from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.mixins import DestroyModelMixin
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet


class APIMixin(BaseMixin):

    filter_backends = (ViewFilterBackend, RangeFilterBackend, RelatedFilterBackend)
    pagination_class = ModulePagination
    paginate_by = 100

    @property
    def model(self):
        if getattr(self, '_model', None):
            return self._model

        try:
            self._model = apps.get_model(self.kwargs.get('app'), self.kwargs.get('model'))
        except LookupError:
            raise Http404

        if not hasattr(self._model, '_bmfmeta'):
            raise Http404

        return self._model

    def get_queryset(self):
        qs = self.model._bmfmeta.filter_queryset(
            self.model.objects.all(),
            self.request.user,
        )
        return qs

    def get_serializer_class(self):
        """
        return the serializer which is registered with the model
        """
        return self.model._bmfmeta.serializer_class


class APIOverView(BaseMixin, APIView):
    """
    All registered modules and views which are viewable by the current user
    """

    def get_view_name(self):
        return 'BMF'

    def get(self, request, format=None):
        """
        """
        site = request.djangobmf_site

        # === Modules ---------------------------------------------------------

        modules = []
        for ct, model in site.models.items():

            info = model._meta.app_label, model._meta.model_name
            perm = '%s.view_%s' % info
            if self.request.user.has_perms([perm]):  # pragma: no branch
                related = dict(
                    [
                        (
                            i.name,
                            ContentType.objects.get_for_model(i.related_model).pk
                        )
                        for i in model._meta.get_fields()
                        if hasattr(i.related_model, '_bmfmeta')
                        and self.request.user.has_perms([
                            '%s.view_%s' % (
                                i.related_model._meta.app_label,
                                i.related_model._meta.model_name,
                            )
                        ])
                    ]
                )
                modules.append({
                    'name': model._meta.verbose_name_plural,
                    'ct': ct,
                    'app': model._meta.app_label,
                    'model': model._meta.model_name,
                    'url': reverse('djangobmf:detail', kwargs={
                        'app_label': model._meta.app_label,
                        'model_name': model._meta.model_name,
                    }),
                    'api': reverse('djangobmf:api', request=request, format=format, kwargs={
                        'app': model._meta.app_label,
                        'model': model._meta.model_name,
                    }),
                    'only_related': model._bmfmeta.only_related,
                    'related': related,
                    'creates': [
                        {
                            "name": i[1],
                            "url": reverse(model._bmfmeta.namespace_api + ':create', kwargs={
                                "key": i[0],
                            }),
                        } for i in model._bmfmeta.create_views
                    ],
                })

        # === Dashboards ------------------------------------------------------

        dashboards = []
        for dashboard in site.dashboards:
            categories = []

            for category in dashboard:
                views = []

                for view in category:
                    # add the view if the user has the permissions to view it
                    if view().check_permissions(self.request):  # pragma: no branch

                        ct = ContentType.objects.get_for_model(view.model)

                        views.append({
                            'name': view.name,
                            'key': view.key,
                            'url': reverse("djangobmf:dashboard", kwargs={
                                'dashboard': dashboard.key,
                                'category': category.key,
                                'view': view.key,
                            }),
                            'ct': ct.pk,
                            'api': reverse('djangobmf:api-view', request=request, format=format, kwargs={
                                'db': dashboard.key,
                                'cat': category.key,
                                'view': view.key,
                            }),
                        })

                if views:  # pragma: no branch
                    categories.append({
                        'name': category.name,
                        'key': category.key,
                        'views': views,
                    })

            if categories:  # pragma: no branch
                dashboards.append({
                    'name': dashboard.name,
                    'key': dashboard.key,
                    'categories': categories,
                })

        # === Templates -------------------------------------------------------

        templates = {
            'list': get_template('djangobmf/api/list.html').render().strip(),
            'detail': get_template('djangobmf/api/detail.html').render().strip(),
        }

        # === Navigation ------------------------------------------------------

        navigation = []

        # === Response --------------------------------------------------------

        return Response({
            'dashboards': dashboards,
            'modules': modules,
            'navigation': navigation,
            'templates': templates,
            'debug': settings.DEBUG,
        })


class APIViewDetail(BaseMixin, APIView):

    def get(self, request, view=None, cat=None, db=None, format=None):
        """
        """

        try:
            view_cls = request.djangobmf_site.get_dashboard(db)[cat][view]
        except KeyError:
            raise Http404

        view = view_cls()
        ct = ContentType.objects.get_for_model(view.model)
        context = {
            'ct': ct.pk,
        }
        if view.check_permissions(self.request):  # pragma: no branch
            html = select_template([
                '%s/%s_bmflist.html' % (
                    view.model._meta.app_label,
                    view.model._meta.model_name
                ),
                'djangobmf/api/default-table.html',
            ]).render().strip()
            context['html'] = html

        return Response(context)


class ViewSet(APIMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet):
    pass


class APIModuleListView(APIMixin, ListModelMixin, CreateModelMixin, GenericAPIView):

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class APIModuleDetailView(APIMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
