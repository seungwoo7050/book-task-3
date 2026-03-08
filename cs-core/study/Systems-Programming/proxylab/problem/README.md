# Proxy Lab Problem Boundary

## Overview

Implement a proxy that:

- accepts client connections
- parses absolute-form HTTP `GET` requests
- opens a connection to the target server
- forwards the response back to the client
- eventually caches small objects in memory

## What Lives Here

This folder is the shared problem contract.

It contains:

- a starter `proxy.c` with TODO markers
- shared `csapp` helper code for sockets and robust I/O
- a reusable driver wrapper that can run the shared local test harness against a proxy binary

The completed implementations live in `../c` and `../cpp`.

## Default Constraints

- support `GET`
- normalize outbound requests to `HTTP/1.0`
- always send `Host`, `User-Agent`, `Connection: close`, and `Proxy-Connection: close`
- ignore `SIGPIPE`
- object cache size limit: 1 MiB
- maximum single cached object: 100 KiB

## Publication Rule

The local origin server and tests are `study/`-owned scaffolding. They are not official course
assets and can be published with the repository.
