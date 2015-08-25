#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
# from django.contrib.contenttypes.models import ContentType
# from django.contrib.contenttypes.fields import GenericForeignKey
# from django.http import HttpResponse

# from djangobmf.core.report import Report as BaseReport


class Renderer(models.Model):
    """
    Model to store informations to generate a report
    """
    key = models.CharField(
        _("Key"),
        max_length=255,
        blank=True,
        null=True,
        editable=False,
        db_index=True,
    )
    name = models.CharField(
        _("Name"), max_length=20, blank=False, null=False,
    )
#   # TODO needs validator
#   options = models.TextField(
#       _("Options"), blank=True, null=False,
#       help_text=_(
#           "Options for the renderer. Empty this field to get all available options with default values"
#       ),
#   )
    modified = models.DateTimeField(_("Modified"), auto_now=True, editable=False,)

    class Meta:
        verbose_name = _('Renderer')
        verbose_name_plural = _('Renderer')
        get_latest_by = "modified"
        abstract = True

    def __str__(self):
        return '%s' % self.name

#   def clean(self):
#       if self.options == "":
#           generator = self.get_generator()
#           self.options = generator.get_default_options().strip()

#   def get_generator(self):
#       from djangobmf.sites import site
#       try:
#           return site.reports[self.reporttype](self.options)
#       except KeyError:
#           return BaseReport()

    # response with generated file
    def render(self, filename, request, context):
        pass
#       generator = self.get_generator()

#       extension, mimetype, data, attachment = generator.render(request, context)

#       response = HttpResponse(content_type=mimetype)

#       if attachment:
#           response['Content-Disposition'] = 'attachment; filename="%s.%s"' % (
#               filename,
#               extension
#           )

#       response.write(data)

#       return response
