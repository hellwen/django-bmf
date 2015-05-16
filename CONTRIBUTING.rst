
Branching Model
***************

We use git flow. If you are not familar with it. please read this article:

http://nvie.com/posts/a-successful-git-branching-model/


Running tests
*************

When you run tests against your own new code, it's useful to
repeat them for different versions of Python and Django. The recommended way to
run tests is to use``tox``::

    # get django BMF from GitHub
    git clone https://github.com/django-bmf/django-bmf.git
    # run the test suite
    tox

You can also run the tests in your specific environment by using the test-runner script directly::

    ./runtests.py

Writing tests
*************

Write Tests for your Applications
========================================

We usually use the django test-client to do a couple of http-requests to test the view classes,
models and forms you write and modify. You can find examples in the ``djangobmf_contrib`` modules.
This type tests usually cover more than 80% of the application-code. It's a good start.

Write Tests for your the BMF-Core
========================================

At the moment the goal is to increase the test coverage. If you like to help us, look at the coverage Report
and write some tests for modules, which have a poor coverage. Or identify a bug with a testcase :)
