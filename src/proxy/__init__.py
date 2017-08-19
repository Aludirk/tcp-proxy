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

import argparse
import pkg_resources
import signal
import socket
import threading

from . import logger
from .proxy import Proxy


shutdownEvent = threading.Event()


def parseArg():
    """Parse the progrm arguements.

    Returns:
        argparse.Namespace: The parsed attributes.
    """
    parser = argparse.ArgumentParser(description="TCP proxy.")

    parser.add_argument("upHost",
                        help="the host of the upstream server for the proxy.",
                        metavar="upstream-host")
    parser.add_argument("upPort",
                        type=int,
                        help="the port of the upstream server for the proxy.",
                        metavar="upstream-port")

    parser.add_argument("-H",
                        "--host",
                        default="",
                        help="the host of the downstream server for the proxy, default is \"\".",
                        metavar="downstream-host",
                        dest="downHost")
    parser.add_argument("-p",
                        "--port",
                        default=5354,
                        type=int,
                        help="the port of the downstream server for the proxy, default is 5354.",
                        metavar="downstream-port",
                        dest="downPort")
    parser.add_argument("-m",
                        "--select-model",
                        default="select",
                        choices=["epoll", "kqueue", "select"],
                        help=("the I/O select method for the socket connections, "
                              "supports [\"epoll\", \"kqueue\", \"select\"], "
                              "default is \"select\".  "
                              "This is platform dependant feature, "
                              "some models may not support on your platform."),
                        metavar="model",
                        dest="select")
    parser.add_argument("-v",
                        "--version",
                        action="version",
                        version="%(prog)s {}".format(pkg_resources.require("tcp-proxy")[0].version))

    return parser.parse_args()


def shutdownHandler(signal, frame):
    """Handler for shutdown process.

    Args:
        signal (int): The signal number.
        frame (frame): Current stack frame.
    """
    shutdownEvent.set()


def main():
    """Main function."""

    # Parse arguments.
    args = parseArg()

    # Set up shutdown handler.
    signal.signal(signal.SIGINT, shutdownHandler)

    # Set up logger.
    logger.setUpLogger()

    try:
        # Start the proxy.
        proxy = Proxy(args.upHost,
                      args.upPort,
                      args.downHost,
                      args.downPort,
                      shutdownEvent,
                      args.select)
        proxy.daemon = True
        proxy.start()

        logger.info("Proxy established: upstream ({}:{}) <-> downstream ({}:{})".
                    format(args.upHost, args.upPort, args.downHost, args.downPort))

        while proxy.is_alive():
            proxy.join(0.05)
        return proxy.err
    except socket.gaierror as e:
        logger.critical("Fail to initialize proxy (socket.gaierror: {}).".format(e))
    except RuntimeError as e:
        logger.critical("\"{}\" is not supported.".format(e))

    return 1
