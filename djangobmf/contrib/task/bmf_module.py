#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.categories import ProjectManagement
from djangobmf.sites import Module
from djangobmf.sites import ViewMixin
from djangobmf.sites import register

from .categories import GoalCategory
from .categories import TaskCategory
from .models import Task
from .models import Goal
# from .permissions import GoalPermission
# from .permissions import TaskPermission
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


@register(category=GoalCategory)
class MyGoals(ViewMixin):
    model = Goal
    slug = 'my'
    name = _("My goals")
    manager = "mygoals"


@register(category=GoalCategory)
class ActiveGoals(ViewMixin):
    model = Goal
    slug = 'active'
    name = _("Active goals")
    manager = "active"


@register(category=GoalCategory)
class ArchiveGoals(ViewMixin):
    model = Goal
    slug = 'archive'
    name = _("Archive")
    manager = "archive"


@register(category=TaskCategory)
class MyTasks(ViewMixin):
    model = Task
    slug = 'my'
    name = _("My tasks")
    manager = "mytasks"


@register(category=TaskCategory)
class Todolist(ViewMixin):
    model = Task
    slug = 'todo'
    name = _("Todolist")
    manager = "todo"


@register(category=TaskCategory)
class AvailableTasks(ViewMixin):
    model = Task
    slug = 'availiable'
    name = _("Availalbe tasks")
    manager = "available"


@register(category=TaskCategory)
class OpenTasks(ViewMixin):
    model = Task
    slug = 'open'
    name = _("Open tasks")
    manager = "active"


@register(category=TaskCategory)
class ArchiveTasks(ViewMixin):
    model = Task
    slug = 'archive'
    name = _("Archive")
