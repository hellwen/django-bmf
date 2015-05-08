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
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    'Topic :: Office/Business :: Groupware',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

# Dynamically calculate the version
version = __import__('djangobmf').get_version()

setup(
    name='django-bmf',
    version=version,
    url="http://www.django-bmf.org/",
    bugtrack_url="https://github.com/django-bmf/django-bmf/issues",
    license='BSD License',
    platforms=['OS Independent'],
    description='Business Management Framework with integrated ERP solution written for django',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    author="Sebastian Braun",
    author_email="sebastian@elmnt.de",
    packages=find_packages(exclude=['sandbox', 'tests']),
    classifiers=CLASSIFIERS,
    install_requires=[
        'django>=1.7',
        'pytz',
        'requests',
        'django-sekizai',
        # 'django-mptt',
        'djangorestframework>=3.1',
        # 'django-haystack',
        'markdown',
    ],
    include_package_data=True,
    zip_safe=False,
#   test_suite='runtests.main',
#   tests_require = [
#       'coverage',
#       'pep8',
#   ],
)
