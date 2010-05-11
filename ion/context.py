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

import inspect
from os.path import join, dirname, splitext, split, exists

from bus import Bus
from settings import Settings
from fs import imp, locate, is_file

class Context(object):
    def __init__(self, root_dir):
        self.bus = Bus()
        self.settings = Settings(root_dir=root_dir)

    def load_settings(self, config_path):
        self.settings.load(config_path)

    @property
    def apps(self):
        return [app for app in self.settings.Ion.apps.strip().split('\n') if app]

    def load_apps(self):
        self.app_paths = {}
        self.app_modules = {}

        for app in self.apps:
            self.app_modules[app] = imp(app)
            app_path = dirname(inspect.getfile(self.app_modules[app]))
            self.app_paths[app] = app_path

    def list_all_media(self):
        """docstring for list_all_media"""
        app_media = {}

        for app_path in self.app_paths.values():
            media_path = join(app_path, 'media')
            for file_name in locate("*.txt", "*.py", "*.css", "*.js", "*.rst", "*.html", "*.ini", root=media_path):
                if not is_file(file_name):
                    continue
                key = file_name.replace(media_path, '')
                app_media[key] = file_name
        return app_media
