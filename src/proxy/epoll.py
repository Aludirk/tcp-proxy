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


class Epoll(_SelectModel):
    def __init__(self):
        _SelectModel.__init__(self)

        self.epoll = select.epoll()
        self.events = None

    def addConnection(self, connection):
        self.epoll.register(connection.fileno(), select.EPOLLIN)

    def removeConnection(self, connection):
        self.epoll.unregister(connection.fileno())

    def wait(self, timeout):
        try:
            self.events = self.epoll.poll(timeout, 1)
            return True
        except select.error as e:
            logger.error("select.epoll.poll failed ({}).".format(e))
            return False

    def loop(self):
        if self.events is not None:
            for fileno, event in self.events:
                if event == select.EPOLLIN:
                    yield fileno
