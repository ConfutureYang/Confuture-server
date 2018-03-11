#!/usr/bin/env python
#
# Copyright 2018 Confuture
#
import select
import const
import TCPServer

DEFAULT_TIMEOUT = 3000

class MainLoop(object):

    def __init__(self):
        self.poll = select.epoll()
        self.handlers = {}


    def bind(self, port):
        tcp_server = TCPServer.TCPServer()
        bind_sock = tcp_server.bind_socket(port)
        self.poll.register(bind_sock.fileno(),const._EPOLLIN)
        self.handlers[bind_sock.fileno()] = tcp_server.handle_event


    def start(self):
        while True:
            events = self.poll.poll(DEFAULT_TIMEOUT)
            if not events:
                continue
            for fd, event in events:
                handler = self.handlers[fd]
                handler(event,self)




