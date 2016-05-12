#!/usr/bin/python
# ex:set fileencoding=utf-8:

import os
import sys

from setuptools import setup, find_packages, Command

CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    'Topic :: Office/Business :: Groupware',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

# Dynamically calculate the version
version = __import__('djangobmf').get_version()


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [dirpath
        for dirpath, dirnames, filenames in os.walk(package)
        if os.path.exists(os.path.join(dirpath, '__init__.py'))]


def get_package_data(package):
    """
    Return all files under the root package, that are not in a
    package themselves.
    """
    walk = [(dirpath.replace(package + os.sep, '', 1), filenames)
        for dirpath, dirnames, filenames in os.walk(package)
        if not os.path.exists(os.path.join(dirpath, '__init__.py'))
        and dirpath[-11:] != '__pycache__'
    ]
    filepaths = []
    for base, filenames in walk:
        filepaths.extend([os.path.join(base, filename) for filename in filenames])
    return {package: filepaths}


setup(
    name='django-bmf',
    version=version,
    url="http://www.django-bmf.org/",
    license='BSD License',
    platforms=['OS Independent'],
    description='Business Management Framework with integrated ERP solution written for django',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    author="Sebastian Braun",
    author_email="sbraun@django-bmf.org",
    packages=get_packages("djangobmf"),
    package_data=get_package_data("djangobmf"),
    classifiers=CLASSIFIERS,
    extras_require={
      'celery': ['celery'],
      'redis': ['redis'],
      'postgres': ['psycopg2'],
    },
    install_requires=[
        'django>=1.8,<1.9.999',
        'djangorestframework>=3.1,<3.4',
        'pycountry==1.19',
        'xhtml2pdf==0.1a3',
        'markdown',
        'pytz',
    ],
    include_package_data=True,
    zip_safe=False,
#   test_suite='runtests.main',
#   tests_require = [
#       'coverage',
#       'pep8',
#   ],
)
