#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.http import Http404
from django.http import HttpResponse
from django.http import FileResponse

# from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from djangobmf.core.filters.document import DocumentFilter
from djangobmf.core.permissions.document import DocumentPermission
from djangobmf.core.pagination import DocumentPagination
from djangobmf.core.serializers.document import DocumentSerializer
from djangobmf.core.views.mixins import BaseMixin
from djangobmf.models import Document
from djangobmf.conf import settings

import os


class View(BaseMixin, ModelViewSet):
    """
    List, upload, update and delete documents
    """
    permission_classes = [DocumentPermission]
    serializer_class = DocumentSerializer
    pagination_class = DocumentPagination
    filter_backends = [DocumentFilter]

    def get_view_name(self):
        return 'Documents'

    def get_queryset(self):
        return Document.objects.all()

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'many': kwargs.get('many', False)
        }
        return self.serializer_class(*args, **kwargs)

    def get_related_object(self):
        if not hasattr(self, 'related_object'):
            if 'model' in self.kwargs and 'app' in self.kwargs and 'pk' in self.kwargs:
                self.related_object = self.get_bmfobject(self.kwargs['pk'])
            else:
                self.related_object = None
        return self.related_object

    def get_object(self):
        if hasattr(self, "object") and self.object:
            return self.object

        queryset = self.get_queryset()

        try:
            obj = queryset.get(pk=self.kwargs['pk'])
        except queryset.model.DoesNotExist:
            raise Http404

        # using the content_object indirectly ensures the filter-option is
        # used to embed permissions for objects
        if obj.content_object:
            self.model = obj.content_object.__class__
            self.related_object = self.get_bmfobject(obj.content_object.pk)
        else:
            self.model = None
            self.related_object = None

        self.check_object_permissions(self.request, obj)

        self.object = obj

        return self.object

    def pre_save(self, obj):
        if self.request.FILES.get('file', None):
            obj.file = self.request.FILES.get('file')

    def perform_create(self, serializer):
        if self.get_related_object():
            serializer.validated_data['is_static'] = False
            serializer.validated_data['content_type'] = self.get_bmfcontenttype()
            serializer.validated_data['content_id'] = self.related_object.pk
        else:
            serializer.validated_data['is_static'] = True

        serializer.save()

    def download(self, request, pk):
        """
        download the document (filestream-response)
        """
        obj = self.get_object()

        if not obj or not obj.file:
            raise Http404

        sendtype = settings.DOCUMENT_SENDTYPE
        filename = os.path.basename(obj.file.name)
        filepath = obj.file.path
        fileuri = obj.file.url

        if not os.path.exists(filepath):
            raise Http404

        if not request.method == "GET":
            return HttpResponse()

        # Nginx (TODO: untested)
        if sendtype == "xaccel" and not settings.DEBUG:
            response = HttpResponse()
            response['Content-Type'] = 'application/force-download'
            response['Content-Disposition'] = 'inline; filename=%s' % filename
            response['X-Accel-Redirect'] = fileuri
            return response

        # Lighthttpd or Apache with mod_xsendfile (TODO: untested)
        if sendtype == "xsendfile" and not settings.DEBUG:
            response = HttpResponse()
            response['Content-Type'] = 'application/force-download'
            response['Content-Disposition'] = 'inline; filename=%s' % filename
            response['X-Sendfile'] = filepath
            return response

        # Serve file with django
        response = FileResponse(obj.file)
        response['Content-Type'] = obj.mimetype
        response['Content-Disposition'] = 'inline; filename=%s' % filename
        response['Content-Length'] = obj.file.size
        return response
