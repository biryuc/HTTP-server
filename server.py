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

        # allocate a server socket, bind it to a port, and then listen for incoming connections
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((self.host, self.port))
        self.s.listen(1)

    def handle_client(self):
        while 1:
            conn, address = self.s.accept()

            # accept an incoming client connection and parse the input data stream into a HTTP request
            request_data = conn.recv(self.buf_size)
            print(request_data)

            # Based on the request's parameters form a response and send it back to the client
            conn.sendall(self.response)
            conn.close()

            # the server continues to perform steps 2 (GET) and 3 (dir list) for as long as the server is running
            # if in multi-thread mode, then fork a thread after we accept a connection
            # and let the child thread handle parsing and responding to the request

http = HTTP_server()
http.handle_client()