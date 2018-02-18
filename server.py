import select
import socket
import threading
import sys

class HTTP_server():

    host = '127.0.0.1'
    port = 8080
    buf_size = 1024
    max_conn = 200

    # temporary response message for testing

    response = b"""\
HTTP/1.0 200 OK
Content-Type: text/html

<!DOCTYPE html>
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

    def __init__(self,threaded=False):

        # allocate a server socket, bind it to a port, and then listen for incoming connections
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((self.host, self.port))

        if threaded:
            self.s.listen(self.max_conn)
        else:
            self.s.listen(1)

        while True:
            threading.Thread(target=self.handle_client, args=(self.s.accept())).start()

    def handle_client(self, connection, address):
        # accept an incoming client connection and parse the input data stream into a HTTP request
        connection.setblocking(False)
        inputs,outputs,errors = select.select([connection],[connection],[])

        message = ''
        for client_input in inputs:
            data = connection.recv(self.buf_size)
            message += str(data)
            
        print(message)

        
        # Based on the request's parameters form a response and send it back to the client
        connection.sendall(self.response)
        #connection.close()

        # the server continues to perform steps 2 (GET) and 3 (dir list) for as long as the server is running
        # if in multi-thread mode, then fork a thread after we accept a connection
        # and let the child thread handle parsing and responding to the request

if __name__ == "__main__":
    #Accept a flag '--threaded' to make the server threaded
    if sys.argv[1] == '--threaded':
        http = HTTP_server(threaded=True)
    else:
        http = HTTP_server()

