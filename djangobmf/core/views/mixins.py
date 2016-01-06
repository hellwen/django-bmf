#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from djangobmf.conf import settings

from rest_framework.exceptions import NotFound
from rest_framework.exceptions import PermissionDenied


class BaseMixin(object):

    def dispatch(self, *args, **kwargs):
        setattr(self.request, 'djangobmf_appconfig', apps.get_app_config(settings.APP_LABEL))
        return super(BaseMixin, self).dispatch(*args, **kwargs)

    def get_bmfcontenttype(self):
        """
        return the contenttype of the bmf_model
        """
        return ContentType.objects.get_for_model(self.get_bmfmodel())

    def get_bmfmodel(self):
        """
        return the model property or loads the model dynamically
        via the url kwargs (app, model) or throws a LookupError
        """
        if getattr(self, 'model', None):
            return self.model

        if 'app' not in self.kwargs or 'model' not in self.kwargs:
            raise LookupError()

        # Raises also a LookupError, when it does not find a model
        self.model = apps.get_model(self.kwargs.get('app'), self.kwargs.get('model'))
        return self.model

    def get_bmfqueryset(self, filter=True):
        if filter:
            return self.get_bmfmodel()._bmfmeta.filter_queryset(
                self.get_bmfqueryset(filter=False),
                self.request.user,
            )
        return self.get_bmfmodel().objects.all()

    def get_bmfobject(self, pk):
        try:
            return self.get_bmfqueryset().get(pk=pk)
        except self.get_bmfmodel().DoesNotExist:
            if self.get_bmfqueryset(filter=False).filter(pk=pk).count():
                raise PermissionDenied(_('You have no permission to access the object'))
            raise NotFound(_("The object can not be found"))
