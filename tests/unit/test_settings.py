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

import ion.settings as sets
from ion import Settings, SettingsSection
from ConfigParser import ConfigParser, NoSectionError, NoOptionError

parser = (Fake("ConfigParser").expects("__init__")
                              .expects("read")
                              .with_args(arg.endswith("config.ini")))

@with_fakes
@with_patched_object(sets, "ConfigParser", parser)
def test_can_create_settings():
    clear_expectations()
    settings = Settings("some_dir")

    assert settings

@with_fakes
@with_patched_object(sets, "ConfigParser", parser)
def test_settings_will_load_config_ini():
    clear_expectations()
    settings = Settings("some_dir")

    settings.load()

@with_fakes
@with_patched_object(sets, "ConfigParser", parser)
def test_settings_will_load_config_ini_retains_config():
    clear_expectations()
    settings = Settings("some_dir")

    settings.load()

    assert settings.config

custom_file_parser = (Fake("ConfigParser").expects("__init__")
                                          .expects("read")
                                          .with_args(arg.endswith("custom.ini")))

@with_fakes
@with_patched_object(sets, "ConfigParser", custom_file_parser)
def test_settings_can_load_custom_file():
    clear_expectations()
    settings = Settings("some_dir")

    settings.load("custom.ini")

    assert settings.config

@with_fakes
@with_patched_object(sets, "ConfigParser", custom_file_parser)
def test_read_attribute_before_load_gives_error():
    clear_expectations()
    settings = Settings("some_dir")

    try:
        assert settings.SomeSection.SomeAttribute
    except RuntimeError, err:
        assert str(err) == "You can't use any settings before loading a config file. Please use the load method."
        return

    assert False, "Should not have gotten this far"

get_attr_parser = (Fake("ConfigParser").expects("__init__")
                                          .expects("read")
                                          .with_args(arg.endswith("config.ini"))
                                          .expects("get")
                                          .with_args("SomeSection", "SomeAttribute")
                                          .returns("attribute_value"))

@with_fakes
@with_patched_object(sets, "ConfigParser", get_attr_parser)
def test_settings_read_attribute_returns_config_read():
    clear_expectations()
    settings = Settings("some_dir")
    settings.load()

    assert settings.SomeSection.SomeAttribute == "attribute_value"

@with_fakes
def test_settings_read_attribute_as_int():
    clear_expectations()

    fake_config = Fake('config')
    fake_config.expects('get').with_args('name', 'setting').returns("10")

    ss = SettingsSection(None, 'name', fake_config)
    assert ss.as_int('setting') == 10

@with_fakes
def test_settings_read_attribute_as_bool():
    clear_expectations()

    fake_config = Fake('config')
    fake_config.expects('get').with_args('name', 'setting_true_1').returns("True")
    fake_config.next_call('get').with_args('name', 'setting_true_2').returns("true")
    fake_config.next_call('get').with_args('name', 'setting_false_1').returns("False")
    fake_config.next_call('get').with_args('name', 'setting_false_2').returns("false")

    ss = SettingsSection(None, 'name', fake_config)
    assert ss.as_bool('setting_true_1')
    assert ss.as_bool('setting_true_2')
    assert not ss.as_bool('setting_false_1')
    assert not ss.as_bool('setting_false_2')

@with_fakes
def test_settings_read_attribute_with_no_section_returns_none():
    clear_expectations()

    fake_config = Fake('config')
    fake_config.expects('get').with_args('name', 'setting_true_1').raises(NoSectionError('name'))
    fake_config.next_call('get').with_args('name', 'setting_true_2').raises(NoOptionError('name', 'setting_true_2'))

    ss = SettingsSection(None, 'name', fake_config)
    assert not ss.as_bool('setting_true_1')
    assert not ss.as_bool('setting_true_2')

