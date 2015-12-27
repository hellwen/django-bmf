#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from .module import ModuleCloneView
from .module import ModuleCreateView
from .module import ModuleDeleteView
from .module import ModuleDetailView
from .module import ModuleFormAPI
from .module import ModuleReportView
from .module import ModuleUpdateView
from .module import ModuleWorkflowView

from .mixins import ModuleViewMixin


__all__ = (
    'ModuleCloneView',
    'ModuleCreateView',
    'ModuleDeleteView',
    'ModuleDetailView',
    'ModuleFormAPI',
    'ModuleReportView',
    'ModuleUpdateView',
    'ModuleWorkflowView',
    'ModuleViewMixin',
)
