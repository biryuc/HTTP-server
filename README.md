# HTTP-server
A basic HTTP  server that supports directory listing, static files,and CGI scripts.

Web server needs to support the following features:

1. Single connection mode (serial) and multiple connection mode (parallel with multiple threads)
    - In single mode, one connection is handled at a time and thus there is no concurrency.
    - In threading mode, a child process/thread is forked after accepting a request and used to handle the request, thus allowing for multiple requests to be processed at the same time.
2. HTTP GET requests with query and header parsing
3. Automatic directory listing (if directory has no index.html then display a list of the directory contents)
4. Static file transport (download/upload files)
5. Basic CGI support by running a sample CGI script on the server side
    - Must involve some form of processing and dynamic content generation. When the CGI script is embedded into a webpage as response, it will be executed by the server side and the results embedded into the response automatically.