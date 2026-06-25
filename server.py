import socket
import http_parser
from router import Router
from response import build_response 

def handle_home(request):
    return (200, "Welcome to my HTTP server", "text/plain")

def handle_about(request):
    return (200, "This is a small project for me to learn and build an HTTP server in pure Python without using any web frameworks.", "text/plain")

router_table = Router()
router_table.add_route("GET", "/", handle_home)
router_table.add_route("GET", "/about", handle_about)

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
        parsed_data = http_parser.parse_request(data)
        print(parsed_data)
        handler = router_table.resolve(parsed_data['method'], parsed_data['path'])
        if handler:
            (status_code, body, content_type) = handler(parsed_data)
            ret_data = build_response(status_code, body, content_type)        
            conn.sendall(ret_data)
        else:
            error_response = build_response(404, "404 Not Found", "text/plain")
            conn.sendall(error_response)
        conn.close()
except KeyboardInterrupt:
    print("\nShutting down.")
    server_socket.close()