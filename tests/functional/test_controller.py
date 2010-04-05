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

from os.path import abspath, join, dirname
import time

import ion.controllers as ctrl
from ion import Server, ServerStatus, Context
from ion.test_helpers import ServerHelper
from ion.controllers import Controller, route

root_dir = abspath(dirname(__file__))

def clear():
    ctrl.__CONTROLLERS__ = []
    ctrl.__CONTROLLERSDICT__ = {}

def test_can_render_template_from_null_template_folder():
    clear()

    class TemplateFolderController(Controller):
        pass

    server = ServerHelper(root_dir, 'controller_config1.ini')

    try:
        controller = server.ctrl(TemplateFolderController)
        content = controller.render_template('test_template.html')

        assert content == "Hello World"
    finally:
        server.stop()

def test_healthcheck_returns_working_when_no_text_found_in_config():
    clear()

    class HealthCheckController(Controller):
        pass

    server = ServerHelper(root_dir, 'controller_config3.ini')

    try:
        controller = server.ctrl(HealthCheckController)

        content = controller.healthcheck()

        assert content == "WORKING"
    finally:
        server.stop()

def test_healthcheck_returns_custom_string_when_no_text_found_in_config():
    clear()

    class HealthCheckController(Controller):
        pass

    server = ServerHelper(root_dir, 'controller_config1.ini')

    try:
        controller = server.ctrl(HealthCheckController)

        content = controller.healthcheck()

        assert content == "CUSTOMTEXT"
    finally:
        server.stop()

