#!/usr/bin/env python
#
# Copyright 2018 Confuture
#

import mainioloop

import const

class SocketStream(object):

    def __init__(self,sock):
        self.sock = sock
        self.sock.setblocking(False)
        self.receive_data = ''
        self.loop = mainioloop.MainLoop()
        self.add_into_loop()

    def handle_event(self,fd,event):

        if event & const._EPOLLIN:
            while True:
                try:
                    data = self.sock.recv(1024)
                except Exception,e:
                    print "error in socketstream {}".format(e)
                    break
                else:
                    if data:
                        self.receive_data = self.receive_data + data
                    else:
                        print "receive_data:{}".format(self.receive_data)
                        self.loop.remove_handler(self.sock)
                        break

    def add_into_loop(self):
        self.loop.add_handler(self.sock,self.handle_event,const._EPOLLIN)