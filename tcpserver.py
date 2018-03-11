#!/usr/bin/env python
#
# Copyright 2018 Confuture
#
import socket
import mainioloop
import socketstream
import const

class TCPServer(object):

    def listen(self,port):
        host = ("",port)
        accept_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        accept_socket.bind(host)
        accept_socket.listen(5)
        accept_socket.setblocking(False)
        self.sock = accept_socket
        self.loop = mainioloop.MainLoop()
        self.loop.add_handler(self.sock,self.handle_connection,const._EPOLLIN)
        self.loop.start()


    def handle_connection(self,fd,event):
        try:
            conn,addr = self.sock.accept()
        except Exception,e:
            print "error in TCPServer:{}".format(e)
        else:
            socketstream.SocketStream(conn)
