=========================
Model ``BMFMeta`` options
=========================

This document explains all the possible 
BMFMeta-options that you can give your model in its internal
``class BMFMeta``.

Available ``BMFMeta`` options
=============================

``only_related``
----------------

Default: ``False``

.. attribute:: Options.only_related

    If ``only_realted = True``, this model won't generate a detail view
    page.

``has_logging``
---------------

Default: ``True``

.. attribute:: Options.has_logging

    If ``has_logging = True``, this model's activity log will
    have entries for created instances and if a instance is changed
    via a workflow transition or the :attr:`~Options.observed_fields` attribute.

``can_clone``
-----------------

Default: ``False``

.. attribute:: Options.can_clone

    Enables if the object can be cloned

``has_comments``
-----------------

Default: ``False``

.. attribute:: Options.has_comments

    Enables comments to models

``only_related``
-----------------

Default: ``False``

.. attribute:: Options.only_related

    If enabled the model won't get a detail-view. This also overwrites all
    features related to a detail-view, such as comments, files and logging.

``has_files``
---------------

Default: ``False``

.. attribute:: Options.has_files

    Enables file-upload to models

``clean``
-------------

Default: ``False``

.. attribute:: Options.clean

    TODO: Explain what this does, why and when you can use this setting

    It has something to do with the model-forms and the saving of data. In some
    special cases the call of an additional clean-method is neccesary. This
    attribute enables the call of an ``bmf_clean``-method, which needs to be
    definied at model level

``observed_fields``
-------------------

Default: ``[]`` (Empty list)

.. attribute:: Options.observed_fields

    Only fields definied in this list are checks for changes

``search_fields``
-------------------

Default: ``[]`` (Empty list)

.. attribute:: Options.search_fields

    TODO: Explain the options and give example, what happens if you search an model with an empty list here?

    If a text-search is needed the fields defined here are searched.


``workflow``
------------

Default: ``DefaultWorkflow``

.. attribute:: Options.workflow

    TODO: Write doc for workflows and reference it here

    Defines the workflow-object connected to you model


``workflow_field_name``
-----------------------

Default: ``state``

.. attribute:: Options.workflow_field_name

    If the model has a workflow (and the workflow has valid transitions)
    a field is added to you model. The field has the name of this attribute.










