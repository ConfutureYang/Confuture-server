#!/usr/bin/env python
#
# Copyright 2018 Confuture
#
import socket
import select
from connection import HTTPConnection

DEFAULT_TIMEOUT = 3000

class MainLoop(object):

    def __init__(self):

        self.poll = select.epoll()
        self.fd_to_socket = {}
        self.fd_to_connection = {}


    def listen(self, port):
        host = ("",port)
        accept_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        accept_socket.bind(host)
        accept_socket.listen(5)
        accept_socket.setblocking(False)
        self.poll.register(accept_socket.fileno(),select.EPOLLIN)
        self.fd_to_socket[accept_socket.fileno()] = accept_socket
        self.accept_socket = accept_socket

    def start(self):
        while True:
            events = self.poll.poll(DEFAULT_TIMEOUT)
            if not events:
                continue
            for fd, event in events:
                sock = self.fd_to_socket[fd]
                if sock == self.accept_socket:
                    conn, address = self.accept_socket.accept()
                    conn.setblocking(False)

                    new_conn = HTTPConnection(conn)

                    self.poll.register(conn, select.EPOLLIN)
                    self.fd_to_socket[conn.fileno()] = conn
                    self.fd_to_connection[conn.fileno()] = new_conn

                elif event & select.EPOLLIN:
                    poll_conn = self.fd_to_connection[fd]
                    while True:
                        try:
                            data = sock.recv(1024)
                        except Exception,e:
                            break
                        else:
                            if not data:
                                self.poll.unregister(fd)
                                self.fd_to_socket.pop(fd)
                                poll_conn = self.fd_to_connection.pop(fd)
                                print poll_conn.receive_data
                                break
                            poll_conn.receive_data = poll_conn.receive_data + data




                elif event & select.EPOLLHUP:
                    pass

                elif event & select.EPOLLOUT:
                    pass

