# TCP Proxy (0.1.0)

- [Introduction](#introduction)
- [Installation](#installation)
  - [Python 3](#python-3)
  - [setuptools](#setuptools)
  - [TCP Proxy](#tcp-proxy)
- [Examples](#examples)
  - [Simple proxy server](#simple-proxy-server)
  - [Simple proxy server with specific downstream](#simple-proxy-server-with-specific-downstream)
  - [Proxy server using epoll event](#proxy-server-using-epoll-event)
- [License](#license)

## Introduction

A proxy server for TCP socket connections in Python 3, it supports the scalable I/O event, epoll and kqueue, for high performance in large number of connections.

## Installation

### Python 3

To install python-3, please follow the instructions in [Python offical site](https://www.python.org/downloads/).

### setuptools

To install setuptools, please follow the instructions in [setuptools](http://pypi.python.org/pypi/setuptools) package site.

### TCP Proxy

```bash
git clone https://github.com/Aludirk/tcp-proxy
cd tcp-proxy
python setup.py install
```

## Examples

### Simple proxy server

To set up a proxy to a remote server `some.domain.com:9999`, and accept connections by `localhost:5354` (default).

```bash
tcp-proxy some.domain.com 9999
```

### Simple proxy server with specific downstream

To set up a proxy to a remote server `some.domain.com:9999`, and accept connections by `192.168.0.100:20000`.

```bash
tcp-proxy -H 192.168.0.100 -p 20000 some.domain.com 9999
```

### Proxy server using epoll event

```bash
tcp-proxy -m epoll some.domain.com 9999
```

## License

This software is licensed under the [GNU GPL v3 license](https://www.gnu.org/copyleft/gpl.html). © 2017 Aludirk Wong
