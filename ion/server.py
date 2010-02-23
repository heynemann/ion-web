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
from os.path import join, abspath, dirname, splitext, split

import cherrypy

from ion.controllers import Controller
from sqlalchemy_tool import metadata, session, mapper
from ion.context import Context
from ion.cache import Cache
from sqlalchemy.exc import DBAPIError

class ServerStatus(object):
    Unknown = 0
    Starting = 1
    Started = 2
    Stopping = 3
    Stopped = 4

class Server(object):
    imp = __import__

    def __init__(self, root_dir, context=None):
        self.status = ServerStatus.Unknown
        self.root_dir = root_dir
        self.context = context or Context(root_dir=root_dir)
        self.template_filters = {}
        self.test_connection_error = None
        self.cache = None

    @property
    def template_path(self):
        templ_path = self.context.settings.Ion.template_path.lstrip("/")
        templ_path = templ_path and abspath(join(self.root_dir, templ_path)) or abspath(join(self.root_dir, 'templates'))
        return templ_path

    def start(self, config_path, non_block=False):
        self.status = ServerStatus.Starting
        self.publish('on_before_server_start', {'server':self, 'context':self.context})

        self.context.load_settings(abspath(join(self.root_dir, config_path)))
        self.cache = Cache(size=1000, age="5s", log=cherrypy.log)

        if self.context.settings.Ion.as_bool('debug'):
            from storm.tracer import debug
            debug(True, stream=sys.stdout)

        self.import_controllers()

        self.run_server(non_block)

        self.status = ServerStatus.Started
        self.publish('on_after_server_start', {'server':self, 'context':self.context})

    def import_template_filters(self):
        if exists(abspath(join(self.root_dir, "template_filters.py"))):
            template_filters = Server.imp("template_filters")
            for filter_method in template_filters:
                for name, func in inspect.getmembers(os.path):
                    if inspect.isfunction(func) and not name.startswith("_"):
                        self.template_filters[name] = func

    def import_controllers(self):
        controller_path = self.context.settings.Ion.controllers_path
        controller_path = controller_path.lstrip("/") or "controllers"
        controller_path = abspath(join(self.root_dir, controller_path))

        sys.path.append(controller_path)

        for filename in os.listdir(controller_path):
            if filename.endswith(".py"):
                Server.imp(splitext(filename)[0])

    def stop(self):
        self.status = ServerStatus.Stopping
        self.publish('on_before_server_stop', {'server':self, 'context':self.context})

        cherrypy.engine.exit()

        self.status = ServerStatus.Stopped
        self.publish('on_after_server_stop', {'server':self, 'context':self.context})

    def get_server_settings(self):
        sets = self.context.settings

        return {
                   'server.socket_host': sets.Ion.host,
                   'server.socket_port': int(sets.Ion.port),
                   'request.base': sets.Ion.baseurl,
                   'tools.encode.on': True, 
                   'tools.encode.encoding': 'utf-8',
                   'tools.decode.on': True,
                   'tools.trailing_slash.on': True,
                   'log.screen': sets.Ion.as_bool('verbose'),
                   'tools.sessions.on': True
               }

    def get_mounts(self, dispatcher):
        sets = self.context.settings
        media_path = sets.Ion.media_path

        if not media_path:
            media_dir = "media"
            media_path = self.root_dir
        else:
            #REFACTOR
            paths = split(media_path)
            media_dir = paths[-1]
            media_path = join(self.root_dir, join(*paths[:-1]).lstrip("/")).rstrip("/")

        protocol = self.context.settings.Db.protocol
        username = self.context.settings.Db.user
        password = self.context.settings.Db.password
        host = self.context.settings.Db.host
        port = int(self.context.settings.Db.port)
        database = self.context.settings.Db.database

        conn_str = self.connstr(protocol, username, password, host, port, database)

        conf = {
            '/': {
                'request.dispatch': dispatcher,
                'tools.staticdir.root': media_path,
                'tools.SATransaction.on': True,
                'tools.SATransaction.dburi':conn_str, 
                'tools.SATransaction.echo': sets.Ion.as_bool('verbose'),
                'tools.SATransaction.convert_unicode': True
            },
            '/media': {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': media_dir
            }
        }

        return conf

    def get_dispatcher(self):
        routes_dispatcher = cherrypy.dispatch.RoutesDispatcher()

        for controller_type in Controller.all():
            controller = controller_type()
            controller.server = self
            controller.register_routes(routes_dispatcher)

        route_name = "healthcheck"
        controller = Controller()
        controller.server = self
        routes_dispatcher.connect("healthcheck", "/healthcheck", controller=controller, action="healthcheck")

        dispatcher = routes_dispatcher
        return dispatcher

    def run_server(self, non_block=False):
        cherrypy.config.update(self.get_server_settings())
        dispatcher = self.get_dispatcher()
        mounts = self.get_mounts(dispatcher)

        self.app = cherrypy.tree.mount(None, config=mounts)

        self.context.use_db = self.test_connection()

        if not self.context.use_db:
#            cherrypy.engine.subscribe('start_thread', self.connect_db)
#            cherrypy.engine.subscribe('stop_thread', self.disconnect_db)
#        else:
            cherrypy.config.update({'tools.SATransaction.on': False})

        cherrypy.engine.start()
        if not non_block:
            cherrypy.engine.block()

    def test_connection(self):
        from sqlalchemy_tool import configure_session_for_app
        configure_session_for_app(self.app)
        try:
            session.execute("select 1 from dual")
        except DBAPIError:
            return False
        return True

    def subscribe(self, subject, handler):
        self.context.bus.subscribe(subject, handler)

    def publish(self, subject, data):
        self.context.bus.publish(subject, data)

#    def connect_db(self, thread_index):
#        cherrypy.thread_data.store = session

#    def disconnect_db(self, thread_index):
#        s = self.storm_stores.pop(thread_index, None)
#        if s is not None:
#            cherrypy.log("Cleaning up store.", "STORM")
#            s.close()
#        else:
#            cherrypy.log("Could not find store.", "STORM")
#        cherrypy.thread_data.store = None

    def connstr(self, protocol, username, password, host, port, database):
        return "%s://%s:%s@%s:%d/%s" % (
            protocol,
            username,
            password,
            host,
            port,
            database
        )
