#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.apps import apps
from djangobmf.conf import settings

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from djangobmf.core.permissions import DetailPermission
from djangobmf.core.views.mixins import BaseMixin


class View(BaseMixin, GenericAPIView):
    permission_classes = [DetailPermission]
    bmfconfig = apps.get_app_config(settings.APP_LABEL)

    def dispatch(self, *args, **kwargs):
        self.get_bmfmodel()
        return super(View, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        obj = self.get_bmfobject(self.kwargs.get('pk', None))
        module = self.get_bmfmodule()
        report, renderer = self.module.get_object_report(self.kwargs.get('slug', None))
        return report(request, object=obj, renderer=renderer)
        print(obj, module, report)
        return Response('REPORT')
