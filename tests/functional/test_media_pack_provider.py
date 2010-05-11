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


import sys
import os
from os.path import abspath, join, dirname, exists
import time
import shutil

import ion.controllers as ctrl
from ion import Server, ServerStatus, Context
from ion.console.providers import PackageMediaProvider
from ion.test_helpers import ServerHelper
from client import *

root_dir = abspath(join(dirname(__file__), 'testapp'))
sys.path.insert(0, root_dir)
root_dir = join(root_dir, 'testapp')

def test_packing_media_works():
    dir_path = abspath(join(os.curdir, 'testbuild'))
    if not exists(dir_path):
        os.mkdir(dir_path)
    try:
        prov = PackageMediaProvider()

        prov.execute(root_dir, None, [dir_path])

        assert exists(join(dir_path, 'js/readme.rst'))
    finally:
        shutil.rmtree(dir_path)