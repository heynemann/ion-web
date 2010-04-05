#!/usr/bin/env python
#-*- coding:utf-8 -*-

from os.path import abspath, join, split, dirname

from ion import Server, ServerStatus, Context

class ServerHelper (object):

    def __init__(self, root_path, config_path, apps=['tests.functional']):
        self.server = Server(root_path, apps=apps)

        self.server.start(config_path, non_block=True)

        while not self.server.status == ServerStatus.Started:
            time.sleep(0.5)

    def ctrl(self, controller):
        _ctrl = controller()
        _ctrl.server = self.server
        return _ctrl

