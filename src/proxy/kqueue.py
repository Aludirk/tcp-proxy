###############################################################################
# Copyright (C) 2017 Aludirk Wong                                             #
#                                                                             #
# This file is part of TCP Proxy.                                             #
#                                                                             #
# TCP Proxy is free software: you can redistribute it and/or modify it        #
# under the terms of the GNU General Public License as published              #
# by the Free Software Foundation, either version 3 of the License, or        #
# (at your option) any later version.                                         #
#                                                                             #
# TCP Proxy is distributed in the hope that it will be useful,                #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
# GNU General Public License for more details.                                #
#                                                                             #
# You should have received a copy of the GNU General Public License           #
# along with TCP Proxy.  If not, see <http://www.gnu.org/licenses/>.          #
###############################################################################

import select

from . import logger
from .select_model import _SelectModel


class Kqueue(_SelectModel):
    def __init__(self):
        _SelectModel.__init__(self)

        self.kqueue = select.kqueue()
        self.events = []
        self.eventList = None

    def addConnection(self, connection):
        self.events.append(select.kevent(connection.fileno(),
                                         select.KQ_FILTER_READ,
                                         select.KQ_EV_ADD))

    def removeConnection(self, connection):
        self.events.remove(select.kevent(connection.fileno(),
                                         select.KQ_FILTER_READ,
                                         select.KQ_EV_ADD))

    def wait(self, timeout):
        try:
            self.eventList = self.kqueue.control(self.events, 1, timeout)
            return True
        except select.error as e:
            logger.error("select.kqueue.control failed ({}).".format(e))
            return False

    def loop(self):
        if self.eventList is not None:
            for event in self.eventList:
                if event.flags & select.KQ_EV_ADD == select.KQ_EV_ADD and \
                   event.filter == select.KQ_FILTER_READ:
                    yield event.ident
