import socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
PORT = 8080
HOST = ''
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print("Server is listening on port", PORT)
try:
    while True:
        conn, addr = server_socket.accept()
        print("Client address is", addr)
        data = conn.recv(1024)
        print(data)
        conn.sendall(b'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 5\r\n\r\nHello')
        conn.close()
except KeyboardInterrupt:
    print("\nShutting down.")
    server_socket.close()