=========================
Writing emails
=========================


Writing emails with django is pretty basic. This framework offers a ``EmailMessage`` class which
provides you to write emails with the template system from django.


``djangobmf.core.email.EmailMessage``
-------------------------------------

This EmailMessage-class uses a template which contains the content blocks ``html``, ``plain``, and ``topic``
to render a ``context``.

https://docs.djangoproject.com/en/dev/topics/email/#the-emailmessage-class

.. attribute:: context

    Default: ``{}``

    Update the context of an EmailMessage-object. When initializing the object updates
    the ``body`` and ``subject`` from the objects attributes and specified templates.


.. attribute:: base_template

    Default: ``djangobmf/email.html``

    Defines the base template which is used to render the email


.. attribute:: template_name

    Default: ``None``

    Defines a template which is used to generate html and plain text versions of the message.
    If the value of this variable is set to ``None`` or
    the template does not exist, we fall back the django's EmailMessage implementation.


.. attribute:: language

    Default: ``None``

    Overwrite the language for the template renderer
