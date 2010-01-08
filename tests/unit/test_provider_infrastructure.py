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

import ion.console.providers as prov

class TestProvider(prov.Provider):
    def __init__(self):
        super(TestProvider, self).__init__("test")

def test_provider_registers_in_the_collection():
    assert prov.__PROVIDERS__
    assert TestProvider in prov.__PROVIDERS__

def test_all_providers_returns_test_provider():
    assert prov.Provider.all()
    assert TestProvider in prov.Provider.all()

def test_provider_key():
    prv = TestProvider()
    assert prv.key == "test"
