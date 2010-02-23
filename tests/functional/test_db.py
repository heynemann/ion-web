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
import ion.sqlalchemy_tool as tool

root_dir = abspath(dirname(__file__))

def clear():
    ctrl.__CONTROLLERS__ = []
    ctrl.__CONTROLLERSDICT__ = {}

def test_invalid_db_settings_result_in_false_context_use_db():
    clear()

    class TemplateFolderController(Controller):
        pass

    server_helper = ServerHelper(root_dir, 'no_db_config.ini')

    assert not server_helper.server.context.use_db
