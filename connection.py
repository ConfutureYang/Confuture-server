#!/usr/bin/env python
#
# Copyright 2018 Confuture
#


class HTTPConnection(object):

    def __init__(self,conn):
        self.conn = conn
        self.receive_data = ''