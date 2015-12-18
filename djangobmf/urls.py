#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

"""
This is a normal urlconf. it is imported from djangobmf.sites.site.get_url, where
the module views get appended by an '^module/' expression
"""

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.utils.timezone import now
from django.views.decorators.cache import cache_page
from django.views.decorators.cache import never_cache
# from django.views.decorators.vary import vary_on_cookie
from django.views.decorators.http import last_modified

from djangobmf import get_version
from djangobmf.sites import site
from djangobmf.views.api import APIViewDetail
from djangobmf.views.api import APIOverView
from djangobmf.views.api import APIModuleListView
from djangobmf.views.api import APIModuleDetailView
from djangobmf.views.configuration import ConfigurationView
from djangobmf.views.configuration import ConfigurationEdit
from djangobmf.views.dashboard import DashboardIndex
from djangobmf.views.dashboard import Redirect
# from djangobmf.views.dashboard import DashboardCategory
# from djangobmf.views.dashboard import DashboardView
from djangobmf.views.wizard import WizardView


VERSION = get_version()

if settings.DEBUG:
    CACHE_TIME = 1
else:
    CACHE_TIME = 86400  # 24h


@cache_page(CACHE_TIME, key_prefix=VERSION)
@last_modified(lambda req, **kw: now())
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
    url(
        r'^$',
        DashboardIndex.as_view(),
        name="dashboard"
    ),
    url(r'^accounts/', include('djangobmf.account.urls')),

    url(r'^router/', include(site.router.urls, namespace="router")),

    url(
        r'^api/$',
        never_cache(
            APIOverView.as_view()
        ),
        name="api",
    ),
    url(
        r'^api/data/(?P<app>[\w-]+)/(?P<model>[\w-]+)/$',
        never_cache(
            APIModuleListView.as_view()
        ),
        name="api",
    ),
    url(
        r'^api/data/(?P<app>[\w_]+)/(?P<model>[\w_]+)/(?P<pk>[0-9]+)/$',
        never_cache(
            APIModuleDetailView.as_view()
        ),
        name="api",
    ),
    url(
        r'^api/view/(?P<db>[\w_]+)/(?P<cat>[\w_]+)/(?P<view>[\w_]+)/$',
        cache_page(CACHE_TIME, key_prefix=VERSION)(
            last_modified(lambda req, **kw: now())(
                APIViewDetail.as_view()
            )
        ),
        name="api-view",
    ),

    # --- Configuration
    url(
        r'^config/$', ConfigurationView.as_view(), name="configuration",
    ),
    url(
        r'^config/(?P<app_label>[\w_]+)/(?P<name>[\w_]+)/$',
        ConfigurationEdit.as_view(), name="configuration",
    ),

    url(
        r'^detail/$',
        Redirect.as_view(), name="detail",
    ),
    url(
        r'^detail/(?P<model_name>[\w_]+)/$',
        Redirect.as_view(), name="detail",
    ),
    url(
        r'^detail/(?P<model_name>[\w_]+)/(?P<app_label>[\w_]+)/$',
        Redirect.as_view(), name="detail",
    ),
    #   r'^detail/' via sites

    # --- Dashboard
    url(
        r'^dashboard/(?P<dashboard>[\w-]+)/$',
        DashboardIndex.as_view(),
        name="dashboard",
    ),
    url(
        r'^dashboard/(?P<dashboard>[\w-]+)/(?P<category>[\w-]+)/(?P<view>[\w-]+)/$',
        DashboardIndex.as_view(),
        name="dashboard",
    ),
    url(
        r'^dashboard/(?P<dashboard>[\w-]+)/(?P<category>[\w-]+)/(?P<view>[\w-]+)/(?P<pk>[0-9]+)/$',
        DashboardIndex.as_view(),
        name="dashboard",
    ),
    #   url(
    #       r'^dashboard/(?P<dashboard>[\w-]+)/(?P<category>[\w-]+)/$',
    #       DashboardCategory.as_view(),
    #       name="dashboard",
    #   ),
    #   r'^dashboard/(?P<dashboard>[\w-]+)/' via sites


    url(r'^document/', include('djangobmf.document.urls')),
    url(r'^i18n/', i18n_javascript, name="jsi18n"),
    #  url(r'^messages/', include('djangobmf.message.urls')),
    url(r'^notifications/', include('djangobmf.notification.urls')),
    url(r'^wizard/$', WizardView.as_view(), name="wizard"),
)
