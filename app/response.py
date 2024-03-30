from enum import Enum
from socket import socket

class StatusCode(Enum):
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


class Response:
    def __init__(self, code: StatusCode):
        self.code = code
        self.response = f"HTTP/1.1 {self.code.value} {self.code.name}\r\n\r\n"
    
    def send(self, conn: socket) -> None:
        conn.send(self.response.encode())

