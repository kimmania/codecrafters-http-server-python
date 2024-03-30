from enum import Enum
from socket import socket
from .response import Response, StatusCode


class RequestMethod(Enum):
    GET = "GET"
    HEAD = "HEAD"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    CONNECT = "CONNECT"
    OPTIONS = "OPTIONS"
    #TRACE = "TRACE"    #Ignoring as no browsers seem to support it
    PATCH = "PATCH"


class Request:
    def __init__(self, raw_data: str, conn: socket):
    # HTTP requests structure and are composed of:
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

        try:
            self.conn = conn
            self.raw_data: str = raw_data
            self.data: list[str] = self.raw_data.split("\r\n") #split into separate lines for processing
            request_line = self.data[0]
            method, self.target, self.version = request_line.split(" ") #gather key pieces of information from the start line
            self.method = RequestMethod(method)
        except Exception:
            Response(StatusCode.BAD_REQUEST).send(conn)

    def respond(self, response: Response) -> None:
        response.send(self.conn)

