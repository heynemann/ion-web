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

import os
from os.path import join, dirname, abspath, exists
from os import walk

import fnmatch

def locate(pattern, root=os.curdir):
    root_path = abspath(root)

    return_files = []
    for path, dirs, files in walk(root_path):
        for filename in fnmatch.filter(files, pattern):
            return_files.append(join(path, filename))
    return return_files
