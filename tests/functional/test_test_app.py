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

import sys
from os.path import abspath, join, dirname
import time

import ion.controllers as ctrl
from ion import Server, ServerStatus, Context
from ion.test_helpers import ServerHelper
from ion.controllers import Controller, route
from client import *

root_dir = abspath(join(dirname(__file__), 'testapp'))
sys.path.insert(0, root_dir)
root_dir = join(root_dir, 'testapp')

def clear():
    ctrl.__CONTROLLERS__ = []
    ctrl.__CONTROLLERSDICT__ = {}

def test_index_action_returns_overriden_template():
    clear()
    import pdb;pdb.set_trace()
    server = ServerHelper(root_dir, 'config.ini')

    try:
        exit_code, content = HttpClient.get('http://localhost:8082/')
        assert exit_code == 200
        assert "TEMPLATE OVERRIDING WORKS" in content
    finally:
        server.stop()
