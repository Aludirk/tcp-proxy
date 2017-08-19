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

from threading import Thread

import socket

from . import logger
from .select_model import createSelection


class Proxy(Thread):
    """A TCP proxy.

    Args:
        upHost (str): The host for upstream.
        upPort (int): The port for upstream.
        downHost (str): The host for downstream.
        downPort (int): The port for downstream.
        stopEvent (threading.Event): The event to signal the termination of the thread.
        selectModel (str): The model for the I/O select, supports:
                           - epoll
                           - kqueue
                           - select
    """
    def __init__(self, upHost, upPort, downHost, downPort, stopEvent, selectModel):
        Thread.__init__(self)

        self.upHost = upHost
        self.upPort = upPort
        self.stopEvent = stopEvent
        self.connection = {}

        # Create selection model.
        try:
            self.select = createSelection(selectModel)
        except AttributeError as e:
            raise RuntimeError(selectModel)

        # Create downstream socket.
        self.downSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.downSock.bind((downHost, downPort))
            self.downSock.listen(5)
            self.select.addConnection(self.downSock)
        except socket.gaierror as e:
            raise e

    def run(self):
        """Thread portal."""
        self.err = 0

        while not self.stopEvent.is_set():
            # Wait I/O signal.
            if not self.select.wait(0.05):
                self.err = 1
                break

            # Loop for the active connections.
            for fd in self.select.loop():
                if fd == self.downSock.fileno():
                    # Create connection.
                    conn, _ = self.downSock.accept()
                    connFd = conn.fileno()

                    upSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    upSock.connect((self.upHost, self.upPort))
                    upSockFd = upSock.fileno()

                    self.select.addConnection(conn)
                    self.connection[connFd] = (conn, upSockFd)

                    self.select.addConnection(upSock)
                    self.connection[upSockFd] = (upSock, connFd)

                    logger.info("New connections - down ({}) <-> up ({}).".format(connFd, upSockFd))
                else:
                    # Proxy data.
                    if fd in self.connection:
                        readSock, writeFd = self.connection[fd]
                    else:
                        continue

                    if writeFd in self.connection:
                        writeSock, _ = self.connection[writeFd]
                    else:
                        continue

                    # Read data.
                    data = readSock.recv(1024)
                    if not data:
                        # Disconnected.
                        del self.connection[fd]
                        self.select.removeConnection(readSock)
                        readSock.close()

                        del self.connection[writeFd]
                        self.select.removeConnection(writeSock)
                        writeSock.close()

                        logger.info("Disconnected - ({}) <-> ({}).".format(fd, writeFd))
                        continue

                    # Wrtie data.
                    writeSock.sendall(data)

        # Clean up all connections.
        for connection in self.connection:
            connection.close()
        self.downSock.close()
