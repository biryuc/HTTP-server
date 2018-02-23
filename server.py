import select
import socket
import threading
import sys
import os
import mimetypes
import time
import subprocess
import re
from urllib.parse import unquote


class HTTP_server:
    host = '127.0.0.1'
    port = 8081
    buf_size = 1024
    max_conn = 200
    abs_path = 'http://' + str(host) + ':' + str(port)
    url_pattern = re.compile('^((\/\w+\.?\w*)+)\??((\w+=\w+[&]?)*)', re.IGNORECASE)

    def __init__(self, threaded=False):

        # allocate a server socket, bind it to a port, and then listen for incoming connections
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
        inputs, outputs, errors = select.select([connection], [], [])

        # Read from socket until input is exhausted
        if inputs:
            request = ''
            while True:
                try:
                    request += connection.recv(self.buf_size).decode()
                except Exception as exp:
                    print(request)
                    break

            response = self.parse_request(request)
            connection.sendall(response)
            connection.close()

    def parse_request(self, request):
        fields = request.split('\r\n')[0].split(' ')
        if fields[0] == 'GET':
            resource = fields[1]
            protocol = fields[2]
            response = self.handle_GET(unquote(resource), protocol)
        else:
            response = 'HTTP/1.0 501 Not Implemented\r\n'

        return response

    def call_cgi(self, cgi, args=[], inputs=None):
        cgi_proc = subprocess.Popen([cgi]+args, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        if inputs:
            output = cgi_proc.communicate(input=inputs)[0]
        else:
            output = cgi_proc.communicate()[0]

        return output

    # First, check if passed path exists:
    # If not: page not found; if yes: need to know if it's a file or dir
    # If file: display it; if directory: check if index.html exists
    # If index.html exists: open; if not: traverse directory

    def handle_GET(self, resource, protocol):

        components = self.url_pattern.match(resource)
        path = '.'+components.group(1)
        arg_string = components.group(3)

        if resource[-4:] == '.cgi':
            if arg_string:
                args = arg_string.replace('&',' ').replace('=',' ').split(' ')
                self.call_cgi(path[:-4], args)
            else:
                self.call_cgi(path[:-4])
            

        if resource == '/favicon.ico':
            return ''.encode()

        response_line = protocol + ' 200 OK\r\n'
        content_line = 'Content-Type: '
        content_type = 'text/html'
        blank_line = '\r\n'

        if not os.path.exists(path):
            body = b'HTTP/1.0 404 Not Found\r\n'
        else:
            if os.path.isdir(path):
                index = path + 'index.html'
                if os.path.exists(index):
                    f = open(index, "r")
                    body = f.read().encode()
                    f.close()
                else:
                    body = self.traverse_dir('.' + resource).encode()

            else:
                # open file that was passed
                c_type, format = mimetypes.guess_type(path)[0].split('/')
                if c_type == 'text':
                    f = open(path, "r")
                    body = f.read().encode()
                    f.close()
                else:
                    content_type = mimetypes.guess_type(path)[0]
                    f = open(path, "rb")
                    body = f.read()
                    f.close()

        header_part = response_line + content_line + content_type + blank_line + blank_line
        response = header_part.encode() + body
        return response

    # Traverse current directory and display all subdirectories and files

    def traverse_dir(self, path):

        # path must end with slash or error occurs
        if path[-1] != '/':
            path = path + '/'

        # make sure we can't go past home directory for server
        # otherwise get a relative path for parent directory

        if path == './':
            parent = './'
        else:
            parent = os.path.dirname(os.path.dirname(path))

        # create html file

        begin = """
        <!DOCTYPE html>
        <html>
        <body>
        """
        header = "<h1>Index of " + path[1:] + "</h1>"

        table_start = """
        <table cols=\"3\" cellspacing=\"10\"> 
            <tr>
                <th>Name</th>
                <th>LastModified</th> 
                <th>Size</th>
            </tr>
        """

        parent_row = self.create_link_col('Parent', self.abs_path + parent[1:])\
                     + self.create_modified_col(parent) + self.create_size_col(parent)

        traversed =  begin + header + table_start + parent_row

        files = os.listdir(path)
        for f in files:
            fpath = path + f
            traversed = traversed + self.create_link_col(f, self.abs_path + fpath[1:])\
                     + self.create_modified_col(fpath) + self.create_size_col(fpath)

        end = """
        </table>
        </body>
        </html>
        """
        return traversed + end

    def create_link_col(self, name, link):
        return '<tr><th align=\"left\" ><a href=\"'+ link +'\">' + name + '</a></th>'

    def create_modified_col(self, path):
        date = time.strftime("%m/%d/%Y %I:%M:%S %p", time.localtime(os.path.getmtime(path)))
        return '<th>' + date + '</th>'

    def create_size_col(self, path):
        if os.path.isfile(path):
            size = str(os.path.getsize(path)) + 'B'
        else:
            size = '-'
        return '<th align=\"right\" >' + size + '</th></tr>'

if __name__ == "__main__":
    # Accept a flag '--threaded' to make the server threaded
    if len(sys.argv) >= 1 and sys.argv[1] == '--threaded':
        http = HTTP_server(threaded=True)
    else:
        http = HTTP_server()
