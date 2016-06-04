#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.sites import register
from djangobmf.sites import Relationship

from .models import Task
from .models import Goal


@register(model_from=Task)
class ProjectTaskRelationship(Relationship):
    name = _("Open Tasks")
    slug = "task"
    field = "task_set"
    model_to = "djangobmf_project.Project"
    settings = "BMF_CONTRIB_PROJECT"
    template = "djangobmf_task/task_related_project.html"

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(
            completed=False,
        )


@register(model_from=Goal)
class ProjectGoalRelationship(Relationship):
    name = _("Active Goals")
    slug = "goal"
    field = "goal_set"
    model_to = "djangobmf_project.Project"
    settings = "BMF_CONTRIB_PROJECT"
    template = "djangobmf_task/goal_related_project.html"

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(
            completed=False,
        )


@register(model_from=Task)
class GoalTasksRelationship(Relationship):
    name = _("Tasks")
    slug = "task"
    field = "task_set"
    model_to = "djangobmf_task.Goal"
    settings = "BMF_CONTRIB_GOAL"
    template = "djangobmf_task/task_related_goal.html"
