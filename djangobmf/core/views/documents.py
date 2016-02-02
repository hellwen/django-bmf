#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.http import Http404
from django.http import HttpResponse
from django.http import FileResponse

# from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from djangobmf.core.filters.documents import DocumentFilter
from djangobmf.core.pagination import DocumentsPagination
from djangobmf.core.serializers.documents import DocumentsSerializer
from djangobmf.core.views.mixins import BaseMixin
from djangobmf.models import Document
from djangobmf.conf import settings

import os


class View(BaseMixin, ModelViewSet):
    """
    List, upload, update and delete documents
    """
    permission_classes = []
    serializer_class = DocumentsSerializer
    pagination_class = DocumentsPagination
    filter_classes = [DocumentFilter]

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

    def filter_queryset(self, queryset):
        return queryset

    def get_object(self):
        if hasattr(self, "object"):
            return self.object

        try:
            self.object = self.filter_queryset(self.get_queryset()).get(pk=self.kwargs['pk'])
        except self.get_queryset().model.DoesNotExist:
            raise Http404

        # using the content_object indirectly ensures the filter-option
        # used to embed permissions for objects
        if self.object.content_object:
            self.related_object = self.get_bmfobject(self.object.content_object.pk)
        else:
            self.related_object = None

        self.check_object_permissions(self.request, self.object)

        return self.object

#   def list(self, request, app=None, model=None, pk=None):
#       """
#       list either unattached files or files attached to another model
#       (depending if ``app`` and ``model`` is set by the request uri)
#       """
#       if app and model and pk:
#           self.related_object = self.get_bmfobject(pk)
#           queryset = self.get_queryset().filter(
#               is_static=False,
#               content_type=self.get_bmfcontenttype(),
#               content_id=self.related_object.pk
#           )
#       else:
#           self.related_object = None
#           queryset = self.get_queryset().filter(
#               is_static=True,
#           )

#       queryset = self.filter_queryset(queryset)

#       serializer = self.get_serializer(queryset, many=True, list=True, request=self.request)

#       return Response(serializer.data)

    def download(self, request, pk):
        """
        download the document (filestream-response)
        """
        obj = self.get_object()

        sendtype = settings.DOCUMENT_SENDTYPE
        filename = os.path.basename(obj.file.name)
        filepath = obj.file.path
        fileuri = obj.file.url

        if not os.path.exists(filepath):
            raise Http404

        # Nginx (untested)
        if sendtype == "xaccel" and not settings.DEBUG:
            response = HttpResponse()
            response['Content-Type'] = 'application/force-download'
            response['Content-Disposition'] = 'attachment; filename=%s' % filename
            response['X-Accel-Redirect'] = fileuri
            return response

        # Lighthttpd or Apache with mod_xsendfile (untested)
        if sendtype == "xsendfile" and not settings.DEBUG:
            response = HttpResponse()
            response['Content-Type'] = 'application/force-download'
            response['Content-Disposition'] = 'attachment; filename=%s' % filename
            response['X-Sendfile'] = filepath
            return response

        # Serve file with django
        response = FileResponse(obj.file)
        response['Content-Type'] = obj.mimetype
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        response['Content-Length'] = obj.file.size
        return response
