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

# Architecture

```text
Browser / curl
      │
      ▼
 TCP Socket Server
      │
      ▼
 HTTP Parser
      │
      ▼
 Router
      │
      ▼
 Route Handler
      │
      ▼
 Response Builder
      │
      ▼
 Client Socket
```

## Request Flow

Every incoming request follows the same pipeline:

### 1. Socket

The server waits for incoming TCP connections using a listening socket. Once a client connects, the operating system creates a new socket dedicated to that client.

```
Browser
    │
    ▼
TCP Socket
```

The server reads the raw bytes sent by the client.

---

### 2. HTTP Parser

The raw bytes are decoded into an HTTP request.

The parser extracts:

* HTTP Method
* Request Path
* HTTP Version
* Headers
* Request Body

For example:

```text
GET /users HTTP/1.1
Host: localhost:8080
User-Agent: curl
```

becomes a structured request object that the rest of the server can use.

---

### 3. Router

The router determines which function should handle the request.

Example:

```text
GET /
        ↓
home_handler()

GET /about
        ↓
about_handler()

POST /login
        ↓
login_handler()
```

Instead of filling the server with large chains of `if` statements, the router maps `(method, path)` pairs to handler functions.

---

### 4. Route Handler

Each handler contains the business logic for a specific endpoint.

Examples include:

* Returning HTML
* Returning JSON
* Reading a file
* Processing form data
* Returning a 404 page

Handlers do not manually construct HTTP messages—they simply return the data that should be sent back.

---

### 5. Response Builder

The response builder converts the handler's output into a valid HTTP response.

It generates:

* Status line
* Headers
* Blank line
* Response body

Example:

```http
HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: 25

<h1>Hello World</h1>
```

---

### 6. Send Response

The completed HTTP response is sent back to the client through the client socket.

After the response has been sent, the connection is closed (or kept alive in future versions).

---

## Server Lifecycle

### 1. Create Socket

A socket object is created and configured for:

* IPv4 (`AF_INET`)
* TCP (`SOCK_STREAM`)

At this point, nothing is bound to an address. The program is simply requesting a TCP socket from the operating system.

### 2. Set Socket Options

```python
SO_REUSEADDR
```

This allows the server to reuse the same port immediately after restarting instead of waiting for the operating system to release it.

### 3. Bind

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

### 4. Listen

The operating system begins accepting incoming connection requests and places them into a queue.

```python
listen(backlog)
```

The `backlog` determines how many pending connections can wait before new connections are refused.

### 5. Accept Loop

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
2. Parses the HTTP request
3. Routes the request
4. Executes the matching handler
5. Builds an HTTP response
6. Sends the response
7. Closes the client connection

---

# HTTP Request Structure

A complete HTTP request consists of three parts.

## 1. Request Line

Always the first line.

```text
METHOD PATH VERSION
```

Example:

```text
GET / HTTP/1.1
```

---

## 2. Headers

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

---

## 3. Body

Everything after the blank line.

* Usually empty for `GET`
* Commonly present for `POST`, `PUT`, and `PATCH`

---

## Delimiters

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

# Features

* TCP socket server
* Raw HTTP request logging
* HTTP request parsing
* Request routing
* Route handler dispatching
* HTTP response generation
* Proper HTTP status codes
* Modular server architecture

---

# How to Run

Start the server:

```bash
python server.py
```

Send a request:

```bash
curl http://localhost:8080
curl http://localhost:8080/
curl http://localhost:8080/about

```

---

# Project Structure

```text
.
├── server.py
├── http_parser.py
├── router.py
└── response.py
```

## `server.py`

Responsible for:

* Creating the TCP socket
* Accepting client connections
* Receiving incoming data
* Passing requests through the server pipeline
* Sending responses back to clients

---

## `http_parser.py`

Responsible for:

* Parsing the HTTP request line
* Extracting headers
* Reading the request body
* Creating a structured request object

---

## `router.py`

Responsible for:

* Mapping `(HTTP method, path)` pairs to handler functions
* Dispatching incoming requests to the appropriate route
* Returning a `None` response when no matching route exists, then server.py decides to send 404 when resolve returns None

---

## `response.py`

Responsible for:

* Constructing valid HTTP responses
* Generating status lines
* Adding response headers
* Calculating `Content-Length`
* Formatting the final response before sending it to the client

---

# References

* RFC 7230 — HTTP/1.1 Message Syntax and Routing
  https://datatracker.ietf.org/doc/html/rfc7230

* RFC 793 — Transmission Control Protocol (TCP)
  https://datatracker.ietf.org/doc/html/rfc793
