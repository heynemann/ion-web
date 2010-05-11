#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
from os.path import abspath, join, split, dirname

from ion import Server, ServerStatus, Context

class ServerHelper (object):

    def __init__(self, root_path, config_path):
        self.server = Server(root_path)

        self.server.start(config_path, non_block=True)

        while not self.server.status == ServerStatus.Started:
            time.sleep(0.5)

    def stop(self):
        self.server.stop()
        self.server = None

    def ctrl(self, controller):
        _ctrl = controller()
        _ctrl.server = self.server
        return _ctrl

