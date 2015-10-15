#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.forms.models import ModelChoiceIterator as DjangoModelChoiceIterator
from django.forms.models import ModelChoiceField as DjangoModelChoiceField


class ModelChoiceIterator(DjangoModelChoiceIterator):

    def __iter__(self):
        if self.field.empty_label is not None:
            yield ("", self.field.empty_label)
        if self.field.cache_choices:
            if self.field.choice_cache is None:
                self.field.choice_cache = [
                    self.choice(obj) for obj in self.queryset.iterator()
                ]
            for choice in self.field.choice_cache:
                yield choice
        else:
            for obj in self.queryset.iterator():
                yield self.choice(obj)

    def __len__(self):
        return (len(self.queryset) + (1 if self.field.empty_label is not None else 0))


class ModelChoiceField(DjangoModelChoiceField):

    def _get_choices(self):
        if hasattr(self, '_choices'):
            return self._choices
        return ModelChoiceIterator(self)
