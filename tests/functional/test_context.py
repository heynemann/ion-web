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
from os.path import abspath, join, dirname
import time

import ion.controllers as ctrl
from ion import Server, ServerStatus, Context
from ion.test_helpers import ServerHelper
from client import *

root_dir = abspath(join(dirname(__file__), 'testapp'))
sys.path.insert(0, root_dir)
root_dir = join(root_dir, 'testapp')

def test_should_list_media_from_all_apps():
    ctx = Context(root_dir)
    ctx.load_settings(join(root_dir,'config.ini'))
    ctx.load_apps()
    
    all_media = ctx.list_all_media()
    assert '/js/readme.rst' in all_media, all_media


def test_media_js_retrieves_the_right_media_file():
    ctx = Context(root_dir)
    ctx.load_settings(join(root_dir,'config.ini'))
    ctx.load_apps()

    all_media = ctx.list_all_media()
    
    test_file = open(all_media['/js/readme.rst'], 'r')
    file_contents =  test_file.read()
    assert 'main app' in file_contents, file_contents
