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

import os
from os.path import join, dirname, abspath, exists
import shutil

from ion.server import Server

__PROVIDERS__ = []
__PROVIDERSDICT__ = {}

class MetaProvider(type):
    def __init__(cls, name, bases, attrs):
        if name not in ('MetaProvider', 'Provider'):
            __PROVIDERS__.append(cls)
            __PROVIDERSDICT__[name] = cls

        super(MetaProvider, cls).__init__(name, bases, attrs)

class Provider(object):
    __metaclass__ = MetaProvider

    @classmethod
    def all(self):
        return __PROVIDERS__

    def __init__(self, key):
        self.key = key

class CreateProjectProvider(Provider):
    def __init__(self):
        super(CreateProjectProvider, self).__init__("create")

    def recursive_copy(self, from_path, to_path):
        shutil.copytree(from_path, to_path)

    def execute(self, current_dir, options, args):
        if not args or not args[0]:
            raise ValueError("You need to pass the project name to be created")

        project_name = args[0]

        new_project_template = abspath(join(dirname(__file__), "new_project"))
        to_project_path = abspath(join(current_dir, project_name))

        if exists(to_project_path):
            raise ValueError("The choosen path(%s) already exists! Please choose a different name or try another folder.")

        self.recursive_copy(new_project_template, to_project_path)

class RunServerProvider(Provider):
    def __init__(self):
        super(RunServerProvider, self).__init__("run")

    def execute(self, current_dir, options, args):
        server = Server(root_dir=current_dir)

        try:
            server.start("config.ini")
        except KeyboardInterrupt:
            server.stop()

class UnitTestProvider(Provider):
    def __init__(self):
        super(UnitTestProvider, self).__init__("unit")

    def execute(self, current_dir, options, args):
        from nose.core import run
        from nose.config import Config

        tests_dir = join(current_dir, "tests", "unit")

        run(argv=["-d", "-s", "--verbose", tests_dir])

