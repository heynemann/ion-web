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
from os.path import join, abspath, dirname, splitext, split, exists
import inspect

import cherrypy
from cherrypy.lib.static import serve_file
from cherrypy.process.plugins import PIDFile

from ion.controllers import Controller
from sqlalchemy_tool import metadata, session, mapper, configure_session_for_app
from ion.context import Context
from ion.cache import Cache
from ion.fs import imp as import_module
from ion.fs import locate, is_file
from sqlalchemy.exc import DBAPIError
import logging

class ServerStatus(object):
    Unknown = 0
    Starting = 1
    Started = 2
    Stopping = 3
    Stopped = 4

class Server(object):
    import_method = __import__

    @classmethod
    def imp(cls, name):
        return import_module(name, Server.import_method)

    def __init__(self, root_dir, context=None):
        self.status = ServerStatus.Unknown
        self.root_dir = root_dir
        self.context = context or Context(root_dir=root_dir)
        self.template_filters = {}
        self.test_connection_error = None
        self.cache = None

    def start(self, config_path, non_block=False):
        self.status = ServerStatus.Starting
        self.publish('on_before_server_start', {'server':self, 'context':self.context})

        self.context.load_settings(abspath(join(self.root_dir, config_path)))
        self.cache = Cache(size=1000, age="5s", log=cherrypy.log)

        self.context.load_apps()
        
        self.apps = self.context.apps
        self.app_paths = self.context.app_paths
        self.app_modules = self.context.app_modules
        
        if self.context.settings.Ion.as_bool('debug'):
            logging.basicConfig()
            logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
            logging.getLogger('sqlalchemy.orm.unitofwork').\
                                                    setLevel(logging.DEBUG)

        self.import_template_filters()
        self.import_controllers()

        if self.context.settings.Ion.pid_file:
            p = PIDFile(cherrypy.engine, self.context.settings.Ion.pid_file)
            p.subscribe()

        self.run_server(non_block)

        self.status = ServerStatus.Started
        self.publish('on_after_server_start', {'server':self, 'context':self.context})

    def import_template_filters(self):

        for app in self.apps:
            template_filters_module = Server.imp("%s.template_filters" %app)
            if template_filters_module:
                for name, func in inspect.getmembers(template_filters_module):
                    if inspect.isfunction(func) and not name.startswith("_"):
                        self.template_filters[name] = func

    def import_controllers(self):
        for app in self.apps:
            ctrl_module = Server.imp(app + '.controllers')
            if not ctrl_module:
                raise RuntimeError('The app %s does not have a controllers module.' % app)

    def stop(self):
        self.status = ServerStatus.Stopping
        self.publish('on_before_server_stop', {'server':self, 'context':self.context})

        cherrypy.engine.exit()
        cherrypy.server.httpserver = None

        self.apps = None
        self.app_paths = None
        self.app_modules = None

        self.status = ServerStatus.Stopped
        self.publish('on_after_server_stop', {'server':self, 'context':self.context})

    def get_server_settings(self):
        sets = self.context.settings

        return {
                   'server.socket_host': sets.Ion.host,
                   'server.socket_port': sets.Ion.as_int('port'),
                   'server.thread_pool': sets.Ion.as_int('threads'),
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
                'tools.SATransaction.on': True,
                'tools.SATransaction.dburi':conn_str, 
                'tools.SATransaction.echo': sets.Ion.as_bool('verbose'),
                'tools.SATransaction.convert_unicode': True
            }
        }

        return conf

    def get_dispatcher(self):
        routes_dispatcher = cherrypy.dispatch.RoutesDispatcher()

        class MediaController():
            def __init__(self, apps):
                self.apps = apps

            def serve_media(self, media_url):
                for app in self.apps:
                    extension = splitext(media_url)[-1]
                    app_module = reduce(getattr, app.split('.')[1:], __import__('testapp'))
                    path = inspect.getfile(app_module)
                    media_path = abspath(join("/".join(split(path)[:-1]), 'media', media_url))

                    if exists(media_path):
                        if extension == ".jpg":
                            content_type = "image/jpeg"
                        elif extension == ".gif":
                            content_type = "image/gif"
                        elif extension == ".png":
                            content_type = "image/png"
                        elif extension == ".js":
                            content_type = "text/javascript"
                        elif extension == ".css":
                            content_type = "text/css"
                        elif extension.startswith('.htm'):
                            content_type = "text/html"
                        else:
                            content_type = "text/plain"

                        return serve_file(media_path, content_type=content_type)

                raise cherrypy.HTTPError(404)

        for controller_type in Controller.all():
            controller = controller_type()
            controller.server = self
            controller.register_routes(routes_dispatcher)

        media_controller = MediaController(self.apps)
        routes_dispatcher.connect("media", "/media/{media_url:(.+)}", controller=media_controller, action="serve_media")

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
            cherrypy.config.update({'tools.SATransaction.on': False})

        cherrypy.engine.start()
        if not non_block:
            cherrypy.engine.block()

    def test_connection(self):
        configure_session_for_app(self.app)
        try:
            session.execute("select 1 from dual")
        except DBAPIError, err:
            msg = '''\n\n============================ IMPORTANT ERROR ============================\nNo connection to the database could be made with the supplied parameters.\nPLEASE VERIFY YOUR CONFIG.INI FILE AND CHANGE IT ACCORDINGLY.\n=========================================================================\n\n'''
            cherrypy.log.error(msg, 'DB')
            self.test_connection_error = err
            return False
        return True

    def subscribe(self, subject, handler):
        self.context.bus.subscribe(subject, handler)

    def publish(self, subject, data):
        self.context.bus.publish(subject, data)

    def connstr(self, protocol, username, password, host, port, database):
        return "%s://%s:%s@%s:%d/%s" % (
            protocol,
            username,
            password,
            host,
            port,
            database
        )
