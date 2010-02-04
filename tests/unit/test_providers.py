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

from ion import Version
import ion.console.providers as providers
from ion.console.providers import *

history = []
old_log = providers.log
def log(message):
    history.append(message)

def setup():
    global history
    providers.log = log
    history = []

def teardown():
    providers.log = old_log

#version provider

def test_can_create_version_provider():
    setup()

    prov = VersionProvider()
    assert prov

    teardown()

def test_version_provider_prints():
    VersionProvider().execute(None, None, None)

def test_version_provider_logs_proper_version():
    setup()

    version_str = "Ion v%s - http://github.com/heynemann/ion\nCreated by Bernardo Heynemann (heynemann@gmail.com)" % Version
    VersionProvider().execute(None, None, None)
    assert history
    assert history[0] == version_str

    teardown()

#help provider

def test_can_create_help_provider():
    setup()

    prov = HelpProvider()
    assert prov

    teardown()

def test_help_provider_logs_help_text():
    setup()

    version_str = "Help to be written"
    HelpProvider().execute(None, None, None)
    assert history
    assert history[0] == version_str

    teardown()

# create project provider
def test_can_create_create_project_provider():
    setup()

    prov = CreateProjectProvider()
    assert prov

    teardown()

custom_locate_1 = Fake(callable=True).with_args("*.txt", "*.py", "*.css", "*.js", "*.rst", "*.html", "*.ini", root="some_path").returns(['test.txt'])
is_file_true = Fake(callable=True).returns(True)
is_file_false = Fake(callable=True).returns(False)
read_all_file = lambda path, contents: Fake(callable=True).with_args(path).returns(contents)
remove_file = lambda path: Fake(callable=True).with_args(path)
replace_file = lambda path, contents: Fake(callable=True).with_args(path, contents)

template = Fake('Template')
template_class = Fake(callable=True).with_args('some_text').returns(template)

@with_fakes
@with_patched_object(providers, "locate", custom_locate_1)
@with_patched_object(providers, "is_file", is_file_true)
@with_patched_object(providers, "read_all_file", read_all_file('test.txt', 'some_text'))
@with_patched_object(providers, "remove_file", remove_file('test.txt'))
@with_patched_object(providers, "replace_file_contents", replace_file('test.txt', 'some_text_1'))
@with_patched_object(providers, "Template", template_class)
def test_create_project_provider_can_replace_tokens_properly():
    setup()
    clear_expectations()

    template.expects('substitute').with_args(project_name="bla").returns("some_text_1")

    prov = CreateProjectProvider()
    prov.replace_tokens('some_path', project_name="bla")

    teardown()

@with_fakes
@with_patched_object(providers, "locate", custom_locate_1)
@with_patched_object(providers, "is_file", is_file_false)
def test_create_project_provider_replace_tokens_skips_folders():
    setup()
    clear_expectations()

    prov = CreateProjectProvider()
    prov.replace_tokens('some_path', project_name="bla")

    teardown()

def test_create_project_provider_raises_value_error_on_no_project_name():
    setup()
    clear_expectations()

    prov = CreateProjectProvider()

    try:
        prov.execute(None, None, None)
    except ValueError, err:
        assert str(err) == "You need to pass the project name to be created"
        return

    assert False, "Shouldn't reach this far"

    teardown()

fake_exists_1 = Fake(callable=True).with_args(arg.endswith("some_path/some_project")).returns(True)
@with_fakes
@with_patched_object(providers, "exists", fake_exists_1)
def test_create_project_provider_raises_when_directory_already_exists():
    setup()
    clear_expectations()

    prov = CreateProjectProvider()

    try:
        prov.execute("some_path", None, ["some_project"])
    except ValueError, err:
        assert str(err).endswith("some_path/some_project) already exists! Please choose a different name or try another folder.")
        return

    assert False, "Shouldn't reach this far"

    teardown()

