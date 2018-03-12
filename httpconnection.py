#!/usr/bin/env python
#
# Copyright 2018 Confuture
#
from socketconnection import SocketConnection
import const

class HttpConnection(SocketConnection):

    def __init__(self,sock):
        super(HttpConnection, self).__init__(sock)

    def handle_event(self,fd,event):
        if event & const._EPOLLIN:
            while True:
                try:
                    data = self.sock.recv(1024)
                except Exception,e:
                    print "error in httpconnection:{}".format(e)
                    break
                else:
                    if data:
                        self.receive_data += data
                        print self.receive_data
                        print "~~~~~~~~~~~~~~~~"
                    else:
                        self.loop.remove_handler(self.sock)
                        break
