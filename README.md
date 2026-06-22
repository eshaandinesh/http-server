# HTTP Server from Scratch

Learning and building an HTTP server in pure Python without using any web frameworks.

## Why?

I wanted to properly understand what happens underneath the abstractions provided by frameworks:

* How sockets are created and bound
* How incoming connections are accepted
* How HTTP requests are parsed
* How route tables work
* How TCP and HTTP communicate with each other

This project was built to answer questions such as:

* How does the OS know which process should receive a packet sent to port `8080`?
* How does a receiver know where one HTTP header ends and another begins?
* How does a server know when the full request has arrived?
* Why do `GET` requests typically have no body while `POST` requests do?

The goal is to learn the fundamentals of networking by implementing them directly.

---

## Architecture

```text
Browser / curl
      ↓  (HTTP - Application Layer)
      ↓  (TCP  - Transport Layer)
      ↓  (IP   - Network Layer)
      ↓  (Ethernet - Link Layer)
```

### Server Lifecycle

#### 1. Create Socket

A socket object is created and configured for:

* IPv4 (`AF_INET`)
* TCP (`SOCK_STREAM`)

At this point, nothing is bound to an address. The program is simply requesting a TCP socket from the operating system.

#### 2. Set Socket Options

```python
SO_REUSEADDR
```

This allows the server to reuse the same port immediately after restarting instead of waiting for the operating system to release it.

#### 3. Bind

The socket claims an address:

```python
(host, port)
```

Using:

```python
"0.0.0.0"
```

or

```python
""
```

allows the server to accept connections on all network interfaces.

Port `8080` is conventionally used for development HTTP servers.

#### 4. Listen

The operating system begins accepting incoming connection requests and places them into a queue.

```python
listen(backlog)
```

The `backlog` determines how many pending connections can wait before new connections are refused.

#### 5. Accept Loop

The server blocks while waiting for incoming connections.

When a client connects:

```python
client_socket, address = server_socket.accept()
```

The OS returns:

* A new socket dedicated to that client
* The client's `(IP, Port)` address

The original socket continues listening for additional connections.

The server then:

1. Reads data from the client socket
2. Processes the request
3. Sends a response
4. Closes the client connection

---

## HTTP Request Structure

A complete HTTP request consists of three parts:

### 1. Request Line

Always the first line:

```text
METHOD PATH VERSION
```

Example:

```text
GET / HTTP/1.1
```

### 2. Headers

Every line following the request line until a blank line.

Format:

```text
Key: Value
```

Example:

```text
Host: localhost:8080
User-Agent: curl/8.0
```

### 3. Body

Everything after the blank line.

* Usually empty for `GET`
* Commonly present for `POST`, `PUT`, and `PATCH`

---

### Delimiters

Headers and body are separated by:

```text
\r\n\r\n
```

Individual header lines are separated by:

```text
\r\n
```

Example:

```text
POST /users HTTP/1.1\r\n
Host: localhost:8080\r\n
Content-Length: 5\r\n
\r\n
Hello
```

---

## Features

### Implemented

* TCP socket server
* Raw HTTP request logging
* Basic HTTP response generation
* HTTP request parsing

### Planned

* Request routing
* Proper HTTP status codes
* Response helpers
* Multiple HTTP methods
* Better error handling
* Static file serving

---

## How to Run

Start the server:

```bash
python server.py
```

Send a request:

```bash
curl http://localhost:8080
```

---

## Project Structure

```text
.
├── server.py
└── http_parser.py
```

### `server.py`

Contains:

* TCP socket server
* Connection handling
* Raw request logging
* HTTP response generation

### `http_parser.py`

Contains:

* HTTP request parsing logic
* Request line extraction
* Header parsing
* Body extraction

---

## References

* RFC 7230 — HTTP/1.1 Message Syntax and Routing
  https://datatracker.ietf.org/doc/html/rfc7230

* RFC 793 — Transmission Control Protocol (TCP)
  https://datatracker.ietf.org/doc/html/rfc793
