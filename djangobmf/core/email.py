#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.core.mail.message import EmailMultiAlternatives
from django.template import Context
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.template.loader_tags import BlockNode
from django.utils.translation import activate
from django.utils.translation import get_language


def get_rendered_node(template, name, context):
    for node in template.template:
        if isinstance(node, BlockNode) and node.name == name:
            return node.render(Context(context))
    return None


class EmailMessage(EmailMultiAlternatives):

    def __init__(self, *args, **kwargs):

        base_template = get_template(
            kwargs.pop('base_template', "djangobmf/email.html")
        )

        template_name = kwargs.pop('template_name', None)
        language = kwargs.pop('language', None)
        old_language = get_language()
        context = kwargs.pop('context', {})

        if language:
            activate(language)

        if template_name:
            try:
                template = get_template(template_name)
            except TemplateDoesNotExist:
                template = None
        else:
            template = None

        super(EmailMessage, self).__init__(*args, **kwargs)

        if template:
            if 'body' not in context:
                context['body'] = self.body
            if 'subject' not in context:
                context['subject'] = self.subject

            self.subject = get_rendered_node(
                template, 'subject', context
            ) or self.subject

            self.body = get_rendered_node(
                template, 'plain', context
            ) or self.body

            html = get_rendered_node(template, 'html', context)
            if html:
                self.attach_alternative(
                    base_template.render(Context({
                        'subject': self.subject,
                        'html': html,
                    })),
                    'text/html',
                )

        if language:
            activate(old_language)
