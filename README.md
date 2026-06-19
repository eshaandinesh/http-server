# HTTP Server from Scratch

Learning and building an HTTP server in pure python without the use of any frameworks

## Why

I wanted to properly learn and understand what goes on within the system, how sockets are created, bound and how they accept connections. How HTTP gets parsed line by line and how the route table works. This is why I started building an HTTP server from scratch to help me understand the TCP and HTTP internals and fundamentals like How does the OS know which process should receive a packet on port 8080, How does a receiver know where one HTTP header ends and another begins, How does a server know when the full request has arrived, Why does a GET request have no body but a POST does?

## Architecture

Your Browser / curl
      ↓  (HTTP — application layer)
      ↓  (TCP  — transport layer)
      ↓  (IP   — network layer)
      ↓  (Ethernet — link layer)

Server Lifecycle:
	1. Create socket
		Nothing is bound to any address yet, its just to tell the OS that a socket with specifications like IPv4 and TCP is wanted
	2. Set socket options
		Using SO_REUSEADDR to tell the os that I want to reuse same port
	3. Bind
		Claiming an address (host, port) tuple, '' or '0.0.0.0' as host to accept connections on all network interfaces. Port 8080 is conventional for dev HTTP servers
	4. Listen
		OS starts accepting incoming connections into a queue. The argument is the backlog, how many pending connections to queue before refusing new ones
	5. Accept loop
		Program pauses here until client connects. When it does it returns 2 things: new socket for that client, (the original socket keeps listening), and clients (ip, port) address
        On that new socket we read what client sent and write back, then close it


## Features


-TCP socket server, raw request logging, HTTP response

-To be added:
    HTTP request parsing
    routing, proper responses

## How to run

```bash
python server.py
curl http://localhost:8080

```

## Project structure

`server.py` - Contains the server code for the TCP socket server, raw request logging, and HTTP response

## References

[RFC 7230](https://datatracker.ietf.org/doc/html/rfc7230)
[RFC 793](https://datatracker.ietf.org/doc/html/rfc793)