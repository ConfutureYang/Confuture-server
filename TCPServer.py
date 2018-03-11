#!/usr/bin/env python
#
# Copyright 2018 Confuture
#
import socket
import const
import connection

class TCPServer(object):

    def bind_socket(self,port):
        host = ("",port)
        accept_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        accept_socket.bind(host)
        accept_socket.listen(5)
        accept_socket.setblocking(False)
        self.sock = accept_socket
        return self.sock

    def handle_event(self, event, loop):
        conn, address = self.sock.accept()
        conn.setblocking(False)
        connec_context = connection.HTTPConnection(conn)
        loop.poll.register(conn.fileno(),const._EPOLLIN)
        loop.handlers[conn.fileno()] = connec_context.handle_event
