from enum import Enum
from socket import socket
from .contenttype import ContentType

class ResponseCode(Enum):
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    INTERNAL_SERVER_ERROR = 500
    NOT_IMPLEMENTED = 501
    HTTP_VERSION_NOT_SUPPORTED = 505

class Response():
    # HTTP response structure is composed of:
    # 1. Status line containing:
        # protocol version, usually HTTP/1.1
        # status code, like 200, 404, or 500
        # status text, a brief, purely informational, textual description of the status code to help a human understand the HTTP message.
    # An optional set of HTTP headers: 
        # a case-insensitive string followed by a colon (':') and 
        # a value whose structure depends upon the header. 
        # The whole header, including the value, consists of one single line, which can be quite long.
        # Header Categories:
            # General headers apply to the message as a whole
            # Response headers, like Accept-Range, give additional information about the server which doesn't fit in the status line.
            # Representation headers like content-type that describe the original format of the message data and any encoding applied
    # An optional body, Bodies can be broadly divided into three categories:
        # Single-resource bodies, consisting of a single file of known length, defined by the two headers: Content-Type and Content-Length.
        # Single-resource bodies, consisting of a single file of unknown length, encoded by chunks with Transfer-Encoding set to chunked.
        # Multiple-resource bodies, consisting of a multipart body, each containing a different section of information. These are relatively rare.


    def __init__(self, code: ResponseCode):
        self.status = ResponseHeader(code)
        self.headers: list[str] = []
        self.body = ResponseBody()

    # Build the response object
    def __str__(self) -> str:
        # eventually will need to update to include other headers
        header_portion = [str(self.status)] + self.body.representationHeaders()
        return f'{'\r\n'.join(header_portion)}\r\n\r\n{self.body}'
    
    # Send the response
    def send(self, conn: socket) -> None:
        temp = str(self).encode()
        conn.send(temp)

    # todo: add header

    # set the body's content including the content type used in the header
    def setContent(self, text: str, type: ContentType) -> "Response":
        self.body.setContent(text, type)
        return self

    # Set the response code
    def setCode(self, code: ResponseCode) -> "Response":
        self.status = ResponseHeader(code) 
        return self  
   
# Tracks the response code, version, and eventually the headers
class ResponseHeader():
    def __init__(self, code: ResponseCode):
        self.code = code
        self.version = 'HTTP/1.1'
    
    def __str__(self) -> str:
        return f'{self.version} {self.code.value} {self.code.name}'
        
# The body tracks the content type and the length that will be included in the headers section of the response
class ResponseBody():
    def __init__(self):
        self.content = ''
        self.content_type = ContentType.NONE

    def __str__(self):
        if self.content_type == ContentType.NONE:
            return ''
        return self.content
    
    def setContent(self, content: str, content_type: ContentType) -> None:
        self.content = content
        self.content_type = content_type
    
    # provid the additional content headers based on the contents of the body (content type, content length)
    def representationHeaders(self) -> list[str]:
        if self.content_type == ContentType.NONE:
            return []
        return [f'Content-Type: {self.content_type.value}',f'Content-Length: {len(self.content)}']
