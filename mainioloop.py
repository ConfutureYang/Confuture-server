#!/usr/bin/env python
#
# Copyright 2018 Confuture
#
import select
import const
import acceptsocket

DEFAULT_TIMEOUT = 3000

class MainLoop(object):

    def __init__(self):
        self.poll = select.epoll()
        self.handlers = {}


    def bind(self, port):
        accept_sock = acceptsocket.AccpetSocket()
        accept_sock = accept_sock.bind_socket(port)
        self.poll.register(accept_sock.fileno(),const._EPOLLIN)
        self.handlers[accept_sock.fileno()] = accept_sock.handle_event


    def start(self):
        while True:
            events = self.poll.poll(DEFAULT_TIMEOUT)
            if not events:
                continue
            for fd, event in events:
                handler = self.handlers[fd]
                handler(event,self)




