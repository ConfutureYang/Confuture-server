#!/usr/bin/env python
#
# Copyright 2018 Confuture
#
import select
import const
import tcpserver

DEFAULT_TIMEOUT = 3000

class MainLoop(object):

    __instance = None

    def __new__(cls, *args, **kwargs):
        if MainLoop.__instance == None:
            MainLoop.__instance = object.__new__(cls, *args, **kwargs)
            MainLoop.__instance.initialize()
        return  MainLoop.__instance

    def initialize(self):
        self.select_poll = select.epoll()
        self.handlers = {}

    def start(self):
        while True:
            events = self.select_poll.poll(DEFAULT_TIMEOUT)
            if not events:
                continue
            for fd,event in events:
                handler = self.handlers[fd]
                handler(fd,event)

    def add_handler(self,conn,func,event):
        self.select_poll.register(conn.fileno(),event)
        self.handlers[conn.fileno()] = func

    def remove_handler(self,conn):
        self.select_poll.unregister(conn.fileno())
        self.handlers.pop(conn.fileno())

