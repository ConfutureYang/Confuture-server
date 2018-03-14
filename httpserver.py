#!/usr/bin/env python
#
# Copyright 2018 Confuture
#
from tcpserver import TCPServer
import httpconnection


class HttpServer(TCPServer):
    def handle_connection(self,fd,event):
        try:
            conn,addr = self.sock.accept()
        except Exception,e:
            print "error in TCPServer:{}".format(e)
        else:
            httpconnection.HttpConnection(conn)
