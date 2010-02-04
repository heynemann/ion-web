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

fake_shutil_1 = Fake("shutil")
@with_fakes
@with_patched_object(fs, 'shutil', fake_shutil_1)
def test_recursive_copy():
    clear_expectations()

    fake_shutil_1.expects('copytree').with_args("a", "b")

    fs.recursive_copy("a","b")

@with_fakes
@with_patched_object(fs, 'shutil', fake_shutil_1)
def test_move_dir():
    clear_expectations()

    fake_shutil_1.expects('move').with_args("a", "b")

    fs.move_dir("a","b")

fake_file_1 = Fake('file')
fake_open_1 = Fake(callable=True).with_args("a", "r").returns(fake_file_1)
@with_fakes
@with_patched_object(fs, 'open_file', fake_open_1)
def test_read_all_text():
    clear_expectations()

    fake_file_1.expects('read').returns('some text')
    fake_file_1.expects('close')

    text = fs.read_all_file("a")

    assert text == "some text"

fake_file_2 = Fake('file')
fake_open_2 = Fake(callable=True).with_args("a", "w").returns(fake_file_2)
@with_fakes
@with_patched_object(fs, 'open_file', fake_open_2)
def test_replace_file_contents():
    clear_expectations()

    fake_file_2.expects('write').with_args('text to write')
    fake_file_2.expects('close')

    fs.replace_file_contents("a", "text to write")

fake_remove_1 = Fake(callable=True).with_args("a")
@with_fakes
@with_patched_object(fs, 'remove', fake_remove_1)
def test_remove_file():
    clear_expectations()

    fs.remove_file("a")

fake_is_file_1 = Fake(callable=True).with_args("a").returns(True)
@with_fakes
@with_patched_object(fs, 'isfile', fake_is_file_1)
def test_is_file():
    clear_expectations()

    assert fs.is_file("a")


