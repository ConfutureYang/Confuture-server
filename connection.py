#!/usr/bin/env python
#
# Copyright 2018 Confuture
#
import const

class HTTPConnection(object):

    def __init__(self,conn):
        self.conn = conn
        self.receive_data = ''

    def handle_event(self,event,loop):

        if event & const._EPOLLIN:
            while True:
                try:
                    data = self.conn.recv(1024)
                except Exception,e:
                    print e
                    break
                else:
                    if data:
                        self.receive_data += data
                    else:
                        loop.poll.unregister(self.conn.fileno())
                        print "all_data = {}".format(self.receive_data)
                        break