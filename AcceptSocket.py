#!/usr/bin/env python
#
# Copyright 2018 Confuture
#
import socket
import const
from platform import kqueue

_DEFAULT_BACKLOG = 128

class AcceptSocket(object):
    def __init__(self):
        self.sockets = {}
        self.handlers = {}

    def listen(self,port):
        hosts = ("",port)
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.bind(hosts)
        sock.listen(_DEFAULT_BACKLOG)
        sock.setblocking(False)
        self.sockets[sock.fileno()] = sock
        self.handlers[sock.fileno()] = self.accpet_handler

        kq = kqueue.KQueue()
        kq.register(sock.fileno(),const.READ)

        import time
        while True:
            events = kq.poll()
            print events
            for event in events:
                fd = event.ident
                event_sock = self.sockets[fd]
                flag = event.flags
                if flag & const.READ:
                    callback = self.handlers[fd]
                    accept_sock = self.sockets[fd]
                    print "accept_sock = {} fileno = {}".format(accept_sock,accept_sock.fileno())
                    callback(accept_sock,kq)

                if flag & const.WRITE:
                    message = "hello confuture"
                    event_sock.sendall(message)

            time.sleep(3)

    def accpet_handler(self, sock, kqueue):
        for i in range(_DEFAULT_BACKLOG):
            try:
                conn,addr = sock.accept()
                conn.setblocking(False)
                # self.recv_handler(conn)
                self.handlers[conn.fileno()] = self.recv_handler
                kqueue.register(conn.fileno(), const.READ)
                print "conn = {}, conn.fileno()={}".format(conn,conn.fileno())
            except socket.error as e:
                pass


    def recv_handler(self, sock, kqueue= None):
        buffer = sock.recv(2048)
        print "receive buffer:{}".format(buffer)




if __name__ == "__main__":
    accept_sock = AcceptSocket()
    accept_sock.listen(8001)
