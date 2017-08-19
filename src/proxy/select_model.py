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

from abc import ABCMeta, abstractmethod


def createSelection(model):
    """The select model factory.

    Args:
        model (str): The model supported:
                     - epoll
                     - kqueue
                     - select
    Returns:
       _SelectModel: The specific select model.
    """
    if "epoll" == model:
        from .epoll import Epoll
        return Epoll()
    elif "kqueue" == model:
        from .kqueue import Kqueue
        return Kqueue()
    elif "select" == model:
        from .select import Select
        return Select()


class _SelectModel(metaclass=ABCMeta):
    """The model for socket I/O selection."""
    def __init__(self):
        pass

    @abstractmethod
    def addConnection(self, connection):
        """Add socket connection.

        Args:
            connection (socket.socket): The socket connection to add.
        """
        pass

    @abstractmethod
    def removeConnection(self, connection):
        """Remove socket connection.

        Args:
            connection (socket.socket): The socket connection to remove.
        """
        pass

    @abstractmethod
    def wait(self, timeout):
        """Waiting the I/O signal from sockets.

        Args:
            timeout (float): Time in second for the waiting to timeout.

        Returns:
            bool: Whether has any errors during the waiting period.
        """
        pass

    @abstractmethod
    def loop(self):
        """A generator for the active sockets.

        Returns:
            int: The fileno of the active socket connection.
        """
        pass
