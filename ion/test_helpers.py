#!/usr/bin/env python
#-*- coding:utf-8 -*-

from os.path import abspath, join, split, dirname

from ion import Server, ServerStatus, Context

class ServerHelper (object):

    def __init__(self, config_path):
        self.server = Server(abspath(dirname(config_path)))

        self.server.start(split(config_path)[-1], non_block=True)

        while not self.server.status == ServerStatus.Started:
            time.sleep(0.5)

    def ctrl(self, controller):
        _ctrl = controller()
        _ctrl.server = self.server
        _ctrl.context = self.server.context
        return _ctrl

