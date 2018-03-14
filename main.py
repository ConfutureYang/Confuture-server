#!/usr/bin/env python
#
# Copyright 2018 Confuture
#

import httpserver

http_server = httpserver.HttpServer()
httpserver.listen(8888)