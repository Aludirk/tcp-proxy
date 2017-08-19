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

import logging
import sys
import time


def setUpLogger():
    """Set up the loggers for logging."""
    root = logging.getLogger()
    root.setLevel(logging.NOTSET)

    formatter = logging.Formatter("%(asctime)sGMT : %(message)s")
    logging.Formatter.converter = time.gmtime

    # Set up output logger.
    output = logging.getLogger("stdout")
    outputHander = logging.StreamHandler(sys.stdout)
    outputHander.setFormatter(formatter)
    output.setLevel(logging.NOTSET)
    output.addHandler(outputHander)

    # Set up error logger.
    error = logging.getLogger("stderr")
    errorHandler = logging.StreamHandler()
    errorHandler.setFormatter(formatter)
    error.setLevel(logging.WARN)
    error.addHandler(errorHandler)


def critical(message):
    """Log with critical severity level.

    Args:
        message (str): The message to log.
    """
    logger = logging.getLogger("stderr")
    logger.critical(message)


def error(message):
    """Log with error severity level.

    Args:
        message (str): The message to log.
    """
    logger = logging.getLogger("stderr")
    logger.error(message)


def warning(message):
    """Log with warning severity level.

    Args:
        message (str): The message to log.
    """
    logger = logging.getLogger("stderr")
    logger.warning(message)


def info(message):
    """Log with info severity level.

    Args:
        message (str): The message to log.
    """
    logger = logging.getLogger("stdout")
    logger.info(message)


def debug(message):
    """Log with debug severity level.

    Args:
        message (str): The message to log.
    """
    logger = logging.getLogger("stdout")
    logger.debug(message)
