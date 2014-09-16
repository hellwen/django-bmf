#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.apps import apps


def model_from_name(name):
    app, modelname = name.split('.')

    if not apps.is_installed(app):
        return None

    return apps.get_model(app, modelname)
