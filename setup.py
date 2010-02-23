#!/usr/bin/env python
#-*- coding:utf-8 -*-

# Copyright Bernardo Heynemann <heynemann@gmail.com>

# Licensed under the Open Software License ("OSL") v. 3.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.opensource.org/licenses/osl-3.0.php

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ion import Version
from setuptools import setup, find_packages

setup(
    name = 'Ion',
    version = Version,
    description = "Ion is an MVC Web Framework",
    long_description = """Ion is an MVC Web Framework.""",
    keywords = 'MVC Web Framework',
    author = 'Bernardo Heynemann',
    author_email = 'heynemann@gmail.com',
    url = 'http://www.ionwebframework.org',
    license = 'OSI',
    classifiers = ['Development Status :: 4 - Beta',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved',
                   'Natural Language :: English',
                   'Operating System :: MacOS',
                   'Operating System :: Microsoft :: Windows',
                   'Operating System :: POSIX :: Linux',
                   'Programming Language :: Python :: 2.6',],
    packages = ['ion'],
    include_package_data=True,
    package_data = {
        '': ['*.txt'],
        '': ['*.rst'],
        '': ['*.html'],
        '': ['*.py'],
    },
    install_requires=[
        "cherrypy",
        "jinja2",
        "sqlalchemy",
        "routes",
        "nose"
    ],
    entry_points = {
        'console_scripts': [
            'ion = ion.console.ion_console:main',
        ],
    },
)

