#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.http import Http404

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from djangobmf.core.pagination import DocumentsPagination
from djangobmf.core.serializers import DocumentsSerializer
from djangobmf.core.views.mixins import BaseMixin
from djangobmf.models import Document

# import os


class View(BaseMixin, ViewSet):
    """
    List, upload, update and delete documents
    """
    # permission_classes = [ActivityPermission]
    serializer_class = DocumentsSerializer
    pagination_class = DocumentsPagination

    def get_view_name(self):
        return 'Documents'

    def get_queryset(self):
        return Document.objects.all()

    def get_object(self, pk):
        if hasattr(self, "object"):
            return self.object

        try:
            self.object = self.get_queryset().get(pk=pk)
        except self.get_queryset().model.DoesNotExist:
            raise Http404

        # using the content_object indirectly ensures the filter-option
        # used to embed permissions for objects
        self.related_object = self.get_bmfobject(self.object.content_object.pk)

        return self.object

    def list(self, request, app=None, model=None, pk=None):
        """
        list either unattached files or files attached to another model
        (depending if ``app`` and ``model`` is set by the request uri)
        """
        if app and model and pk:
            self.related_object = self.get_bmfobject(pk)
            queryset = self.get_queryset().filter(
                is_static=False,
                content_type=self.get_bmfcontenttype(),
                content_id=self.related_object.pk
            )
        else:
            self.related_object = None
            queryset = self.get_queryset().filter(
                is_static=True,
            )
        return Response(queryset.objects.values_list('pk', flat=True))

    def list_customer(self, request):
        """
        """
        pass

    def list_project(self, request):
        """
        """
        pass

    def create(self, request, app=None, model=None, pk=None):
        """
        create a new file - attached to a document, if ``model`` and ``app``
        is set by the request uri
        """
        return Response('Not implemented')

    def detail(self, request, pk):
        """
        get the details of a document
        """
        obj = self.get_object(pk)
        return Response('Not implemented %s' % obj.pk)

    def destroy(self, request, pk):
        """
        delete a document
        """
        obj = self.get_object(pk)
        return Response('Not implemented %s' % obj.pk)

    def update(self, request, pk):
        """
        update the document
        """
        obj = self.get_object(pk)
        return Response('Not implemented %s' % obj.pk)

    def update_file(self, request, pk):
        """
        update only the file of the document
        """
        obj = self.get_object(pk)
        return Response('Not implemented %s' % obj.pk)

    def download(self, request, pk):
        """
        download the document (filestream-response)
        """
        obj = self.get_object(pk)
        return Response('Not implemented %s' % obj.pk)

'''
from django.views.static import serve
from djangobmf.signals import activity_addfile
from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden, Http404
from django.views.static import serve
def sendfile(request, fileobject, allowed=True):
  if not allowed and not request.user.is_superuser:
    return HttpResponseForbidden()

  if not fileobject:
    return Http404

  sendtype = getattr(settings,"BMF_DOCUMENTS_SEND",None)

  if sendtype == "accelredirect" and not settings.DEBUG:
    response = HttpResponse()
    response['Content-Type'] = ''
    response['X-Accel-Redirect'] = fileobject.url # TODO not tested if this works with apache
    return response

  if sendtype == "sendfile" and not settings.DEBUG:
    response = HttpResponse()
    response['Content-Type'] = ''
    response['X-Sendfile'] = (os.path.join(settings.BMF_DOCUMENTS_ROOT, fileobject.url)).encode('utf-8')
    return response

  # serve with django
  return serve(request,fileobject.url[len(settings.BMF_DOCUMENTS_URL):],document_root=settings.BMF_DOCUMENTS_ROOT)
'''
