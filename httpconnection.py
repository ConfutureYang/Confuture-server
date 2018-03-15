#!/usr/bin/env python
#
# Copyright 2018 Confuture
#
from socketconnection import SocketConnection
import const
import url

class HttpConnection(SocketConnection):

    def __init__(self,sock):
        self.request_line = ''
        self.request_method = ''
        self.request_uri = ''
        self.http_version = ''
        self.request_header = {"Content-Length":0} # give Content-Length default value 0
        self.request_body = ''
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
                    status = self.receive_data_over(data)
                    if status == 'stop':
                        self.stop()
                        break
                    elif status == 'disconnect':
                        self.disconnect()
                        break



    def receive_data_over(self,data):
        if data:
            self.receive_data += data
            if not self.request_line:
                if "\r\n\r\n" in self.receive_data:
                    space_line_index = self.receive_data.index('\r\n\r\n')
                    request_header = self.receive_data[0:space_line_index]
                    for index,line in enumerate(request_header.split('\r\n')):
                        if index == 0:
                            self.request_line = line
                            self.request_method,self.request_uri,self.http_version = line.split(" ")
                        else:
                            key,value = line.split(": ")
                            self.request_header[key] = value
                    self.receive_data = self.receive_data[space_line_index+4:]

            body_length = int(self.request_header['Content-Length'])
            if body_length == len(self.receive_data):
                self.request_body = self.receive_data
                self.receive_data = ''
                return 'stop'
            else:
                return 'receive'

        else:
            return 'disconnect'

    def stop(self):
        self.handle_request()
        self.printHttpConnectionInformation()

    def disconnect(self):
        self.printHttpConnectionInformation()
        self.loop.remove_handler(self.sock)

    def handle_request(self):
        for uri,request_fun in url.URLS:
            if uri == self.request_uri:
                response_data = request_fun(self)
                http_response_data = self.create_http_response(response_data)
                self.sock.sendall(http_response_data)
                print "resonponse successfully"
                return
        print "response failed"


    def printHttpConnectionInformation(self):
        print "self.request_method:{}".format(self.request_method)
        print "self.request_uri:{}".format(self.request_uri)
        print "self.http_version:{}".format(self.http_version)
        print "self.request_header:{}".format(self.request_header)
        print "self.request_body:{}".format(self.request_body)
        print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

    def create_http_response(self,response_data):
        response_line = 'HTTP/1.1 200 OK\r\n'
        headers = {'Content-Type':'application/json; charset=UTF-8'}
        response_headers = ''
        for key,value in headers.items():
            header_line = key +": " +value + '\r\n'
            response_headers += header_line
        return response_line + response_headers + '\r\n' + response_data

