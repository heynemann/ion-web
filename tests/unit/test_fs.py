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

import ion.fs as fs

custom_abspath = Fake(callable=True).with_args('.').returns('test')
custom_walk = Fake(callable=True).with_args('test').returns(((".", [], []),))

@with_fakes
@with_patched_object(fs, 'abspath', custom_abspath)
@with_patched_object(fs, 'walk', custom_walk)
def test_locate_returns_empty_list_when_no_files_found_in_recursive_mode():
    clear_expectations()

    assert not fs.locate('test')

custom_abspath2 = Fake(callable=True).with_args('.').returns('test')
custom_walk2 = Fake(callable=True).with_args('test').returns(((".", ['test', 'test'], ['some_file','test']),))
@with_fakes
@with_patched_object(fs, 'abspath', custom_abspath2)
@with_patched_object(fs, 'walk', custom_walk2)
def test_locate_returns_list_when_files_found_in_recursive_mode():
    clear_expectations()

    result = fs.locate('test')

    assert result == ['./test']
