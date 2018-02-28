#!/usr/bin/env python
#
# Copyright 2018 Confuture
#
import select
import const

class KQueue(object):
    def __init__(self):
        self._kqueue = select.kqueue()

    def register(self, fd, event):
        kevents = []

        if event & const.READ:
            print  "register read fd:{}".format(fd)
            kevents.append(select.kevent(fd, filter=select.KQ_FILTER_READ, flags=select.KQ_EV_ADD))

        if event & const.WRITE:
            kevents.append(select.kevent(fd, filter=select.KQ_FILTER_WRITE, flags=select.KQ_EV_ADD))

        for kevent in kevents:
            self._kqueue.control([kevent], 0)

    def poll(self, timeout = 15):
        events = self._kqueue.control(None, 1000, timeout)
        return events