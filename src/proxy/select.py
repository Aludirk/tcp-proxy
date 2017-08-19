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


class Select(_SelectModel):
    def __init__(self):
        _SelectModel.__init__(self)

        self.readList = []
        self.readable = None

    def addConnection(self, connection):
        self.readList.append(connection)

    def removeConnection(self, connection):
        self.readList.remove(connection)

    def wait(self, timeout):
        try:
            self.readable, _, _ = select.select(self.readList, [], [], timeout)
            return True
        except select.error as e:
            logger.error("select.select failed ({}).".format(e))
            return False

    def loop(self):
        if self.readable is not None:
            for connection in self.readable:
                yield connection.fileno()
