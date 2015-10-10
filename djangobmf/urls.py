#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

"""
This is a normal urlconf. it is imported from djangobmf.sites.site.get_url, where
the module views get appended by an '^module/' expression
"""

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.utils import timezone
from django.views.decorators.cache import cache_page
from django.views.decorators.http import last_modified

from djangobmf import get_version
from djangobmf.views import ModuleOverviewView
from djangobmf.views.api import APIModuleListView
from djangobmf.views.api import APIModuleDetailView
from djangobmf.views.configuration import ConfigurationView
from djangobmf.views.configuration import ConfigurationEdit
from djangobmf.views.dashboard import DashboardView


@cache_page(86400, key_prefix='bmf-js18n-%s' % get_version())
@last_modified(lambda req, **kw: timezone.now())
def i18n_javascript(request):
    """
    Displays the i18n JavaScript that the Django admin requires.
    """
    if settings.USE_I18N:  # pragma: no cover
        from django.views.i18n import javascript_catalog
    else:  # pragma: no cover
        from django.views.i18n import null_javascript_catalog as javascript_catalog
    return javascript_catalog(request, packages=['djangobmf'])


urlpatterns = patterns(
    '',
    url(r'^$', DashboardView.as_view(), name="dashboard"),
    url(r'^accounts/', include('djangobmf.account.urls')),

    #   r'^api/module/' via sites

    # --- Configuration
    url(
        r'^config/$', ConfigurationView.as_view(), name="configuration",
    ),
    url(
        r'^config/(?P<app_label>[\w_]+)/(?P<name>[\w_]+)/$',
        ConfigurationEdit.as_view(), name="configuration",
    ),

    #   r'^detail/' via sites

    # --- Dashboard
    url(
        r'^dashboard/(?P<dashboard>[\w-]+)/$',
        DashboardView.as_view(),
        name="dashboard",
    ),
    #   r'^dashboard/(?P<dashboard>[\w-]+)/' via sites

    # --- REST API
    url(
        r'^rest/(?P<app>[\w-]+)/(?P<model>[\w-]+)/',
        APIModuleListView.as_view(),
        name="rest",
    ),
    url(
        r'^rest/(?P<app_label>[\w_]+)/(?P<model>[\w_]+)/(?P<model>[0-9]+)/',
        APIModuleDetailView.as_view(),
        name="rest",
    ),

    url(r'^document/', include('djangobmf.document.urls')),
    url(r'^i18n/', i18n_javascript, name="jsi18n"),
    #  url(r'^messages/', include('djangobmf.message.urls')),
    url(r'^modules/$', ModuleOverviewView.as_view(), name="modules"),
    url(r'^notifications/', include('djangobmf.notification.urls')),
    url(r'^wizard/', include('djangobmf.wizard.urls')),
)
