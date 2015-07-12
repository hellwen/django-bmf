#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.formats import date_format
from django.utils.translation import ugettext_lazy as _

from djangobmf.categories import ViewFactory
from djangobmf.categories import ProjectManagement
from djangobmf.sites import Module
from djangobmf.sites import site
from djangobmf.sites import register

# from djangobmf.contrib.project.categories import ProjectCategory
# from djangobmf.contrib.project.models import Project

from .categories import GoalCategory
from .categories import TaskCategory
from .models import Task
from .models import Goal
from .permissions import GoalPermission
from .permissions import TaskPermission
from .serializers import GoalSerializer
from .serializers import TaskSerializer
from .views import GoalCloneView
from .views import GoalDetailView


@register(dashboard=ProjectManagement)
class TaskModule(Module):
    model = Task
    serializer = TaskSerializer


@register(dashboard=ProjectManagement)
class GoalModule(Module):
    model = Goal
    clone = GoalCloneView
    detail = GoalDetailView
    serializer = GoalSerializer


@register(dashboard=ProjectManagement)
class GoalCategoryCLS(GoalCategory):
    my = ViewFactory(
        model=Goal,
        name=_("My goals"),
        manager="mygoals",
    )
    active = ViewFactory(
        model=Goal,
        name=_("Active goals"),
        manager="active",
    )
    archive = ViewFactory(
        model=Goal,
        name=_("Archive"),
    )


@register(dashboard=ProjectManagement)
class TaskCategoryCLS(TaskCategory):
    my = ViewFactory(
        model=Task,
        name=_("My tasks"),
        manager="mytasks",
    )
    todo = ViewFactory(
        model=Task,
        name=_("Todolist"),
        manager="todo",
    )
    available = ViewFactory(
        model=Task,
        name=_("Availalbe tasks"),
        manager="available",
    )
    open = ViewFactory(
        model=Task,
        name=_("Open tasks"),
        manager="active",
    )
    archive = ViewFactory(
        model=Task,
        name=_("Archive"),
    )
