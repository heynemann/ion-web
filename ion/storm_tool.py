#!/usr/bin/env python
#-*- coding:utf-8 -*-

# Code obtained from http://tools.cherrypy.org/wiki/Storm with permission granted in the page

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

from traceback import format_exc

import types

import cherrypy

## The database commit tool. This will try to auto-commit on each request.
def do_commit():
    try:
        if not cherrypy.request.rolledback:
            cherrypy.thread_data.store.commit()
    except:
        cherrypy.thread_data.store.rollback()
        cherrypy.log("ROLLBACK - " + format_exc(), "STORM")

def try_commit():
    if cherrypy.response.stream:
        cherrypy.request.hooks.attach('on_end_request', do_commit)
    else:
        if isinstance(cherrypy.response.body, types.GeneratorType):
            cherrypy.response.collapse_body()
        do_commit()

class StormHandlerWrapper(object):
    # to_skip = (KeyboardInterrupt, SystemExit, cherrypy.HTTPRedirect)
    # Nando Florestan does not think the above line is correct,
    # because transactions should never be interrupted in the middle:
    to_skip = [cherrypy.HTTPRedirect]
    
    def __init__(self):
        self.nexthandler = cherrypy.request.handler
        cherrypy.request.handler = self

    def __call__(self, *args, **kwargs):
        try:
            cherrypy.request.rolledback = False
            result = self.nexthandler(*args, **kwargs)
        except Exception, e:
            if not isinstance(e, tuple(self.to_skip)):
                cherrypy.log("ROLLBACK - " + format_exc(), "STORM")
                cherrypy.thread_data.store.rollback()
                cherrypy.request.rolledback = True
            raise
        return result

class StormTool(cherrypy.Tool):
    def _setup(self):
        if cherrypy.request.config.get('tools.staticdir.on', False) or \
            cherrypy.request.config.get('tools.staticfile.on', False):
                return

        cherrypy.request.hooks.attach('before_handler', StormHandlerWrapper, priority=100)
        cherrypy.Tool._setup(self)

cherrypy.tools.storm = StormTool('on_end_resource', try_commit)

