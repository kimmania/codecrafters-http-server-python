from enum import Enum

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
    method: str
    version: str
    path: str
    path_components: list[str] = []
    headers: dict[str, str] = {}
    body: list[str] = []
    endpoint: str

    def __init__(self, raw_data: str):    
        lines = raw_data.split("\r\n")
        if len(lines) == 0:
            raise ValueError("Request is poorly formed")
        start_line = lines.pop(0)
        parts = start_line.split(" ")
        if len(parts) != 3:
            raise ValueError("Request does not have required format")
        if parts[2] != "HTTP/1.1":
            raise ValueError("Wrong http verion")
        self.method = RequestMethod(parts[0])
        self.version = parts[2]
        self.path = parts[1]
        self.path_components = [c for c in self.path.split("/") if c]

        # process headers
        while len(lines) > 0:
            line = lines.pop(0) #grab the next line
            
            if line == '':
                # exit, the loop 
                break

            if ":" in line:
                #have a header, parse it
                key, value = line.split(":", 1)
                self.headers[key.strip().lower()] = value.strip()

        # anything else will be the body
        self.body = "\r\n".join(lines)

        if len(self.path_components) > 0:
            self.endpoint = f'{self.method.name} {self.path_components[0]}'
        else:
            self.endpoint = f'{self.method.name} '

    def getHeaderValue(self, key: str) -> str:
        if key in self.headers:
            return self.headers[key]
        else:
            return None
