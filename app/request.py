from enum import Enum
from socket import socket
from .response import Response, ResponseCode

Max_BUFFER_SIZE = 1024

class RequestMethod(Enum):
    GET = "GET"
    HEAD = "HEAD"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    CONNECT = "CONNECT"
    OPTIONS = "OPTIONS"


class Request:
    # HTTP requests structure is composed of:
    # 1. A request line describing the requests to be implemented. This is always a single line composed of:
        # HTTP method
        # request target
        # HTTP Version
    # 2. An optional set of HTTP headers: 
        # a case-insensitive string followed by a colon (':') and 
        # a value whose structure depends upon the header. 
        # The whole header, including the value, consists of one single line, which can be quite long.
        # Header Categories:
            # General headers apply to the message as a whole
            # Request headers, like user-agent or accept
            # Representation headers like content-type that describe the original format of the message data and any encoding applied
    # 3. A blank line indicating all meta-information for the request has been sent.
    # 4. An optional body containing data associated with the request (like content of an HTML form). 
        # The presence of the body and its size is specified by the start-line and HTTP headers.
        # Bodies can be broadly divided into two categories:
            # Single-resource bodies, consisting of one single file, defined by the two headers: Content-Type and Content-Length.
            # Multiple-resource bodies, consisting of a multipart body, each containing a different bit of information. 
            # This is typically associated with HTML Forms.
    
    def __init__(self, conn: socket):
        self.conn = conn
        self.raw_data = conn.recv(Max_BUFFER_SIZE).decode()
        self.data: list[str] = self.raw_data.split("\r\n") #split into separate lines for processing
        self.header = RequestHeader(self.data) #send the lines to process the header
        self.response = Response(ResponseCode.INTERNAL_SERVER_ERROR) # set up as the default response and replace if successful

    # update the response code
    def status(self, code: ResponseCode) -> "Request":
        self.response.setCode(code)
        return self

    # set the response text
    def text(self, text: str) -> "Request":
        self.response.setText(text)
        return self
    
    # end the response by sending
    def end(self) -> None:
        self.response.send(self.conn)

    # the path requested    
    def path(self) -> str:
        return self.header.path
    
    # request verb
    def method(self) -> RequestMethod:
        return self.header.method
    
    def getHeaderValue(self, key: str) -> str:
        if key in self.header.headers:
            return self.header.headers[key]
        return ""


class RequestHeader:
    def __init__(self, request: list[str]):
        requestLine = request.pop(0)
        method, self.path, self.version = requestLine.split(" ") #gather key pieces of information from the start line
        self.method = RequestMethod(method)

        #grab the headers
        self.headers = {}
        while len(request) > 0:
            line = request.pop(0) #grab the next line
            
            if line == '':
                # exit, the loop 
                break

            if ":" in line:
                #have a header, parse it
                key, value = line.split(":", 1)
                self.headers[key.strip().lower()] = value.strip()
