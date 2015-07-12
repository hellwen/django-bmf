#!/usr/bin/python
# ex:set fileencoding=utf-8:

from fabric.api import *
from fabric.contrib import files

import os

BASEDIR = os.path.dirname(env.real_fabfile)

PYTHON = BASEDIR + "/virtenv/bin/python"
DEVELOP = BASEDIR + "/develop.py"

from djangobmf.demo import FIXTURES

APPS = [
    'accounting',
    'address',
    'customer',
    'employee',
    'invoice',
    'position',
    'product',
    'project',
    'quotation',
    'task',
    'taxing',
    'team',
    'timesheet',
]


@task
def static():
    """
    update static files
    """
    js()
    css()
    with lcd(BASEDIR):
        local('cp bower_components/bootstrap/fonts/glyphicons* djangobmf/static/djangobmf/fonts/')


@task
def css():
    """
    recreate css files - with lessc and yui-compressor
    """
    with lcd(BASEDIR):
        local('lessc less/djangobmf.less > bootstrap.css')
        local('yui-compressor --type css -o djangobmf/static/djangobmf/css/djangobmf.min.css bootstrap.css')
        local('rm bootstrap.css')


@task
def js():
    """
    recreate js files for development and production
    """
    with lcd(BASEDIR):
        js_ext = (
            'bower_components/jquery-cookie/jquery.cookie.js',
            'bower_components/jquery-treegrid/js/jquery.treegrid.js',
            'bower_components/bootstrap/dist/js/bootstrap.js',
        )
        js_own = (
            'js/variables.js',
            'js/bmf-autocomplete.js',
            'js/bmf-calendar.js',
            'js/bmf-editform.js',
            'js/bmf-buildform.js',
            'js/menu.js',
        )

        local('cp bower_components/jquery/dist/jquery.min.js djangobmf/static/djangobmf/js/')
        local('cp bower_components/jquery/dist/jquery.min.map djangobmf/static/djangobmf/js/')
        local('cp bower_components/angular/angular.min.js djangobmf/static/djangobmf/js/')
        local('cp bower_components/angular/angular.min.js.map djangobmf/static/djangobmf/js/')

        local('cp bower_components/bootstrap/dist/js/bootstrap.min.js djangobmf/static/djangobmf/js/')

        local('yui-compressor --type js -o djangobmf/static/djangobmf/js/jquery.cookie.min.js bower_components/jquery-cookie/jquery.cookie.js')
        local('yui-compressor --type js -o djangobmf/static/djangobmf/js/jquery.treegrid.min.js bower_components/jquery-treegrid/js/jquery.treegrid.js')

        local('cat %s > djangobmf/static/djangobmf/js/djangobmf.js' % ' '.join(js_ext + js_own))
        local('yui-compressor --type js -o djangobmf/static/djangobmf/js/djangobmf.min.js djangobmf/static/djangobmf/js/djangobmf.js')
        local('cat %s > djangobmf/static/djangobmf/js/djangobmf.js' % ' '.join(js_own))


@task
def test(fast=False):
    """
    Tests code with django unittests
    """
    with lcd(BASEDIR):
        if fast:
            local('virtenv/bin/coverage run runtests.py -v2 --failfast')
        else:
            local('virtenv/bin/coverage run runtests.py -v2')
        local('virtenv/bin/coverage report -m')


@task
def test_mod(app):
    with lcd(BASEDIR):
        local('virtenv/bin/coverage run runtests.py -v2 --contrib %(app)s' % {'app': app})
        local('virtenv/bin/coverage report -m --include="djangobmf/contrib/%(app)s/*"' % {'app': app})


@task
def test_core(module=""):
    with lcd(BASEDIR):
        local('virtenv/bin/coverage run runtests.py %s -v2 --nocontrib' % module)
        local('virtenv/bin/coverage report -m --omit="djangobmf/contrib/*"')


@task
def locale():
    with lcd(BASEDIR + '/djangobmf'):
        local('%s %s makemessages -l %s --domain django' % (PYTHON, DEVELOP, 'en'))
        local('%s %s makemessages -l %s --domain djangojs' % (PYTHON, DEVELOP, 'en'))
        check_locale()

    for app in APPS:
        with lcd(BASEDIR + '/djangobmf/contrib/' + app):
            local('%s %s makemessages -l %s --domain django' % (PYTHON, DEVELOP, 'en'))
            check_locale()

    with lcd(BASEDIR):
        local('tx pull')

    with lcd(BASEDIR + '/djangobmf'):
        local('%s %s compilemessages' % (PYTHON, DEVELOP))

    for app in APPS:
        with lcd(BASEDIR + '/djangobmf/contrib/' + app):
            local('%s %s compilemessages' % (PYTHON, DEVELOP))

    puts("Dont forget to run 'tx push -s' to push new source files")

def check_locale():
    numstat = local('git diff --numstat locale', quiet)
    for stats in numstat.split('\n'):
        insertions, deletions, file = stats.split('\t')
        if insertions == '1' and deletions == '1' and file[-3:] == '.po':
            with lcd(BASEDIR):
                local('git checkout -- %s' % file)

@task
def make(data=''):
  """
  """
  with lcd(BASEDIR):
    local('rm -f sandbox/database.sqlite')
    local('%s %s migrate --noinput' % (PYTHON, DEVELOP))
    if not data:
        local('%s %s loaddata %s' % (PYTHON, DEVELOP, ' '.join(FIXTURES)))
    else:
        local('%s %s loaddata fixtures/users.json' % (PYTHON, DEVELOP))


@task
def start():
  """
  """
  with lcd(BASEDIR):
    local('%s %s runserver 8000' % (PYTHON, DEVELOP))


@task
def shell():
  """
  """
  local('%s %s shell' % (PYTHON, DEVELOP))
