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

from setuptools import setup, find_packages

import re

# Get the version string.
exec(open("version.py").read())

# Update version in `README.md`.
with open("README.md", "r") as readme:
    lines = readme.readlines()
with open("README.md", "w") as readme:
    readme.write(re.sub(r"\d+\.\d+\.\d+", __version__, lines.pop(0)))
    for line in lines:
        readme.write(line)

# Set up application.
setup(name="tcp-proxy",
      version=__version__,
      author="Aludirk Wong",
      author_email="aludirkwong@gmail.com",
      url="https://github.com/Aludirk/tcp-proxy",
      description="TCP proxy.",
      long_description=("A proxy server for TCP socket connections in Python 3, "
                        "it supports the scalable I/O event, epoll and kqueue, for "
                        "high performance in large number of connections."),
      platforms=["Linux", "MacOS X"],
      license="GNU GPL v3 license",
      packages=find_packages("src"),
      package_dir={"": "src"},
      entry_points={"console_scripts": ["tcp-proxy = proxy:main"]})
