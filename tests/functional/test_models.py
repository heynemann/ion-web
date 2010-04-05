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

from client import HttpClient
from models import *

root_dir = abspath(dirname(__file__))

def clear():
    ctrl.__CONTROLLERS__ = []
    ctrl.__CONTROLLERSDICT__ = {}

def test_save_and_render_user_model():
    clear()

    class TemplateFolderController(Controller):
        @route("/")
        def some_action(self):
            all_users = self.store.query(User).all()
            for user in all_users:
                self.store.delete(user)
            self.store.commit()

            user = User("someone")
            self.store.add(user)

            return str(user)

    server = ServerHelper(root_dir, 'controller_config1.ini')

    exit_code, content = HttpClient.get("http://localhost:9947/")
    assert content == "<User('someone')>"

