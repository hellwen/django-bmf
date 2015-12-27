#!/usr/bin/python
# ex:set fileencoding=utf-8:

from django.core.serializers.json import DjangoJSONEncoder

from djangobmf.currency import BaseCurrency
from djangobmf.workflow import WorkflowContainer


class DjangoBMFEncoder(DjangoJSONEncoder):
    """
    JSONEncoder subclass that knows how to encode currencies
    """

    def default(self, o):
        if isinstance(o, BaseCurrency):
            return str(o.value)

        return super(DjangoBMFEncoder, self).default(o)
