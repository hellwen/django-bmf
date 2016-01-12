
|Build status| |PyPi version| |PyPi downloads| |Python version| |PyPi wheel| |Project license|

Django BMF understands itself as a ERP-Framework with the following design concepts:

* KISS-Principe for endusers
* Fast and easy configuration for people with medium know-how
* Highly customizeable with as few lines of code as possible for application developers

Features
===========================

* Functionality as a django application
  - for an easy integration into an existing django project
  - to make the development of modules easy
  - for the benefit to use a module in an different place of django project (i.e. an online-shop or an customer-interface)
* Login/Logout
* Notifications about activities
* Watch and unwatch models
* File-Upload and document management
* Comments on models
* Information about data-changes
* Behaviour "Django-Admin with custom views"
* Filtering of data and saving the view to a dashboard
* PDF-Reports (very simple and easy to-modify)
* Responsive design -> getbootstrap.com
* Workflows attached to models
  - easy configurable as classes (Workflow, states and transitions)
  - custom functions for transitions
  - integrated into the BMF (i.e you can delete or update a model instance only if the State allows you to do so)
* Each option should be activated and deactivated in die model definition (how needs to append files or write comments to a tax-model?)


Documentation
===========================

.. note::
    Please note that this Project is documented poorly. If you have any questions please contact us!
    We'd love to update the documentation and answer your question!

http://www.django-bmf.org/docs/dev

Demo
===========================

http://demo.django-bmf.org/

Getting Help
===========================

Please report bugs or ask questions using the `Issue Tracker`_ or contact us via team@django-bmf.org

Check also for the latest updates of this project on Github_.

Credits
===========================

* `django`_
* `django-rest-framework`_
* `angularjs`_
* `bootstrap`_

.. _Github: https://github.com/django-bmf/django-bmf
.. _Issue Tracker: https://github.com/django-bmf/django-bmf/issues
.. _django: http://www.djangoproject.com
.. _django-rest-framework: http://www.django-rest-framework.org
.. _angularjs: http://www.angularjs.org
.. _bootstrap: http://www.getbootstrap.com

.. |Build status| image:: https://api.travis-ci.org/django-bmf/django-bmf.svg?branch=develop
   :target: http://travis-ci.org/django-bmf/django-bmf
.. |PyPi version| image:: https://img.shields.io/pypi/v/django-bmf.svg
   :target: https://pypi.python.org/pypi/django-bmf/
.. |PyPi downloads| image:: https://img.shields.io/pypi/dm/django-bmf.svg
   :target: https://pypi.python.org/pypi/django-bmf/
.. |Python version| image:: https://img.shields.io/pypi/pyversions/django-bmf.svg
   :target: https://pypi.python.org/pypi/django-bmf/
.. |PyPi wheel| image:: https://img.shields.io/pypi/wheel/django-bmf.svg
   :target: https://pypi.python.org/pypi/django-bmf/
.. |Project license| image:: https://img.shields.io/pypi/l/django-bmf.svg
   :target: https://pypi.python.org/pypi/django-bmf/
