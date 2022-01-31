#!/usr/bin/env python

from setuptools import setup, find_packages

LONG_DESCRIPTION = '''A flexible way to handle requests within a complex Internal Status Page API application.'''

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules'
]

KEYWORDS = 'api'

setup(
    name='statuspage-agent',
    version='0.3.0',
    description='Flexible requests for Internal Status Page API applications',
    long_description=LONG_DESCRIPTION,
    author='ShinZ Natkid',
    author_email='shinznatkid@gmail.com',
    url='http://github.com/shinznatkid/statuspage-agent',
    packages=find_packages(),
    platforms=['Platform Independent'],
    license='GPLv3',
    classifiers=CLASSIFIERS,
    keywords=KEYWORDS,
    requires=['requests'],
)
