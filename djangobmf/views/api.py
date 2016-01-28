#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

# from django.apps import apps
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
# from django.db.models.fields.related import ManyToOneRel
# from django.db.models.fields.related import ManyToManyField
from django.http import Http404
# from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.template.loader import select_template
from django.utils.translation import ugettext_lazy as _

from djangobmf.models import Notification
from djangobmf.filters import ViewFilterBackend
from djangobmf.filters import RangeFilterBackend
from djangobmf.permissions import ModuleViewPermission
from djangobmf.permissions import NotificationPermission
from djangobmf.pagination import ModulePagination
from djangobmf.core.serializers import NotificationViewSerializer
from djangobmf.core.serializers import NotificationListSerializer
# from djangobmf.core.pagination import NotificationPagination
from djangobmf.views.mixins import BaseMixin

from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
# from rest_framework.mixins import DestroyModelMixin
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from collections import OrderedDict


class ModelMixin(object):

    def get_queryset(self):
        return self.get_bmfqueryset()

    def get_serializer_class(self):
        """
        return the serializer which is registered with the model
        """
        return self.get_bmfmodel()._bmfmeta.serializer_class


class APIIndex(BaseMixin, APIView):
    """
    All registered modules and views which are viewable by the current user
    """

    def get_view_name(self):
        return 'BMF'

    def get(self, request, format=None):
        """
        """
        site = request.djangobmf_site
        appconfig = request.djangobmf_appconfig

        # === Relationships ---------------------------------------------------
        relations = {}
        for relation in appconfig.bmf_relations:

            # check permissions
            perm = '%s.view_%s'

            info = relation._model._meta.app_label, relation._model._meta.model_name
            if not self.request.user.has_perms([perm % info]):
                continue

            info = relation._related_model._meta.app_label, relation._related_model._meta.model_name
            if not self.request.user.has_perms([perm]):
                continue

            ct_target = ContentType.objects.get_for_model(relation._model).pk

            data = OrderedDict([
                ('app_label', relation._related_model._meta.app_label),
                ('model_name', relation._related_model._meta.model_name),
                ('name', relation.name),
                ('slug', relation.slug),
                ('template', relation.template),
            ])

            if ct_target in relations.keys():
                relations[ct_target].append(data)
            else:
                relations[ct_target] = [data]

        # === Modules ---------------------------------------------------------

        modules = []
        for model, module in appconfig.bmf_modules.items():
            ct = ContentType.objects.get_for_model(model).pk

            info = model._meta.app_label, model._meta.model_name
            perm = '%s.view_%s' % info
            if self.request.user.has_perms([perm]):  # pragma: no branch

                modules.append(OrderedDict([
                    ('app', model._meta.app_label),
                    ('model', model._meta.model_name),
                    ('ct', ct),
                    ('name', model._meta.verbose_name_plural),
                    ('watch_function', model._bmfmeta.has_watchfunction),
                    ('data', reverse('djangobmf:api', request=request, format=format, kwargs={
                        'app': model._meta.app_label,
                        'model': model._meta.model_name,
                    })),
                    ('notification', reverse('djangobmf:notification', request=request, format=format, kwargs={
                        'app': model._meta.app_label,
                        'model': model._meta.model_name,
                    })),
                    ('only_related', model._bmfmeta.only_related),
                    ('relations', relations.get(ct, [])),
                    ('creates', [
                        {
                            "name": i[1],
                            "url": reverse(model._bmfmeta.namespace_api + ':create', kwargs={
                                "key": i[0],
                            }),
                        } for i in model._bmfmeta.create_views
                    ]),
                ]))

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
            'notification': get_template('djangobmf/api/notification.html').render().strip(),
        }

        # === Navigation ------------------------------------------------------

        navigation = [
            {
                # verbose (req)
                'name': _('Notifications'),
                'symbol': "glyphicon glyphicon-comment",

                # fallback, when api is unset or does not return html (req)
                'url': reverse('djangobmf:notification'),

                # API call for updates (opt)
                'api': reverse('djangobmf:api-notification', kwargs={'action': 'count'}),

                # check every n seconds for changes (req, when api)
                'intervall': 180,
            },
        ]

        # === Response --------------------------------------------------------

        return Response(OrderedDict([
            ('dashboards', dashboards),
            ('modules', modules),
            ('navigation', navigation),
            ('templates', templates),
            ('ui', OrderedDict([
                ('notification', OrderedDict([
                    ('url', reverse('djangobmf:notification')),
                    ('data', reverse('djangobmf:notification')),
                ])),
            ])),
            ('debug', settings.DEBUG),
        ]))


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
                'djangobmf/api/list-table-default.html',
            ]).render().strip()
            context['html'] = html

        return Response(context)


class ViewSet(ModelMixin, BaseMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet):
    permission_classes = [
        ModuleViewPermission,
    ]
    filter_backends = (ViewFilterBackend, RangeFilterBackend)
    pagination_class = ModulePagination
    paginate_by = 100


class APIModuleListView(ModelMixin, BaseMixin, ListModelMixin, CreateModelMixin, GenericAPIView):
    permission_classes = [
        ModuleViewPermission,
    ]
    filter_backends = (ViewFilterBackend, RangeFilterBackend)
    pagination_class = ModulePagination
    paginate_by = 100

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class APIModuleDetailView(ModelMixin, BaseMixin, RetrieveModelMixin, GenericAPIView):
    permission_classes = [
        ModuleViewPermission,
    ]
    filter_backends = (ViewFilterBackend, RangeFilterBackend)
    pagination_class = ModulePagination
    paginate_by = 100

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class NotificationMixin(BaseMixin):
    permission_classes = [
        NotificationPermission,
    ]

    def get_queryset(self):
        return Notification.objects.filter(
            user=self.request.user,
            watch_ct=self.get_bmfcontenttype(),
        )


class NotificationViewAPI(NotificationMixin, UpdateModelMixin, RetrieveModelMixin, GenericAPIView):
    serializer_class = NotificationViewSerializer

    def get_object(self):
        if 'pk' in self.kwargs:
            self.get_bmfobject(self.kwargs.get('pk'))

        queryset = self.filter_queryset(self.get_queryset())
        lookup = {
            'user': self.request.user,
            'watch_ct': self.get_bmfcontenttype(),
            'watch_id': self.kwargs.get('pk', None),
        }

        try:
            obj = queryset.get(**lookup)
            self.check_object_permissions(self.request, obj)
        except Notification.DoesNotExist:
            obj = Notification(**lookup)
            obj.unread = False
            self.check_permissions(self.request)

        return obj

    def post(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class NotificationListAPI(NotificationMixin, ListModelMixin, GenericAPIView):
    serializer_class = NotificationListSerializer
    pagination_class = ModulePagination

    def get_queryset(self):
        queryset = super(NotificationListAPI, self).get_queryset()
        return queryset.prefetch_related('watch_object').exclude(watch_id__isnull=True)

    def get(self, request, *args, **kwargs):
            return self.list(request, *args, **kwargs)


class NotificationCountAPI(BaseMixin, GenericAPIView):
    def get(self, request, *args, **kwargs):
        data = Notification.objects.filter(
            unread=True,
            user=request.user,
            watch_id__isnull=False,
        ).values_list(
            'watch_ct_id',
        ).annotate(
            count=Count('*'),
        ).order_by(
            'watch_ct_id',
        )
        count = sum([n for ct, n in data])
        return Response(OrderedDict([
            ('active', bool(count)),
            ('count', count),
            ('data', OrderedDict(data)),
        ]))
