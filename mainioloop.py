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
        return  MainLoop.__instance

    def __init__(self):
        self.select_poll = select.epoll()
        self.handlers = {}

    def start(self):
        while True:
            print "start poll"
            events = self.select_poll.poll(DEFAULT_TIMEOUT)
            print "events:{}".format(events)
            for fd,event in events:
                handler = self.handlers[fd]
                handler(fd,event)

    def add_handler(self,conn,func,event):
        print "register fd:{}".format(conn.fileno())
        self.select_poll.register(conn.fileno(),event)
        self.handlers[conn.fileno()] = func

    def remove_handler(self,conn):
        print "unregister fd:{}".format(conn.fileno())
        self.select_poll.unregister(conn.fileno())
        self.handlers.pop(conn.fileno())

