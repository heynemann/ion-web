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

from os.path import abspath, join

from ConfigParser import ConfigParser

class Settings(object):
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.config = None

    def load(self, filename="config.ini"):
        path = abspath(join(self.root_dir, filename))

        self.config = ConfigParser()
        self.config.read(path)

    def __getattr__(self, name):
        if not self.config:
            raise RuntimeError("You can't use any settings before loading a config file. Please use the load method.")

        return SettingsSection(self, name, self.config)

class SettingsSection(object):
    def __init__(self, settings, name, config):
        self.settings = settings
        self.name = name
        self.config = config

    def __getattr__(self, config_name):
        return self.config.get(self.name, config_name)

