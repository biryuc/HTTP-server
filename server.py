import socket
import sys

class HTTP_server():

    host = ''
    port = 10010
    buf_size = 1024

    # temporary response message for testing

    response = b"""\
HTTP/1.0 200 OK

Content-Type: text/html

<html>
    <head>
        <title>Test Page</title>
    </head>
    <body>
        <h1>Level 1 header</h1>
        <h2>Subheading</h2>
        <p>Normal text here</p>
    </body>
</html>
"""

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((self.host, self.port))
        self.s.listen(1)

    def handle_client(self):
        while 1:
            conn, address = self.s.accept()
            request_data = conn.recv(self.buf_size)
            print(request_data)
            conn.sendall(self.response)
            conn.close()


http = HTTP_server()
http.handle_client()