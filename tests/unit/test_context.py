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

from fudge import Fake, with_fakes, with_patched_object, clear_expectations
from fudge.inspector import arg

from ion import Context

def test_can_create_context():
    ctx = Context(root_dir="some")
    assert ctx

def test_context_contains_bus_of_events():
    ctx = Context(root_dir="some")
    assert ctx.bus

def test_context_contains_settings():
    ctx = Context(root_dir="some")
    assert ctx.settings

def test_context_load_settings():
    ctx = Context(root_dir="some")

    ctx.settings = Fake('settings')
    ctx.settings.expects('load').with_args('config.ini')

    ctx.load_settings('config.ini')
