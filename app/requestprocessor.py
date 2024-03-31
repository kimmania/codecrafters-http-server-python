import os
from .contenttype import ContentType
from .webserver import WebServer
from .request import Request
from .response import Response, ResponseCode

class RequestProcessor:
    def upCheck(request: Request, s: WebServer) -> Response:
        print("upcheck")
        return Response(ResponseCode.OK)

    def echo(request: Request, s: WebServer) -> Response:
        print("echo")
        path_suffix = "/".join(request.path_components[1:])
        return Response(ResponseCode.OK).setContent(path_suffix, ContentType.TEXT_PLAIN)

        
    def returnUserAgent(request: Request, s: WebServer) -> Response:
        print("useragent")
        agent = request.getHeaderValue("user-agent")
        if agent == None:
            return Response(ResponseCode.NOT_FOUND)
        
        return Response(ResponseCode.OK).setContent(agent, ContentType.TEXT_PLAIN)

    def getFile(request: Request, s: WebServer) -> Response:
        print("getfile")
        files_in_dir = [
            f
            for f in os.listdir(s.file_directory)
            if os.path.isfile(os.path.join(s.file_directory, f))
        ]
        expected_file = request.path_components[1]
        if expected_file in files_in_dir:
            with open(os.path.join(s.file_directory, expected_file), "r") as f:
                response_body = f.read()
            return Response(ResponseCode.OK).setContent(response_body, ContentType.APPLICATION_OCTET_STREAM)
        else:
            return Response(ResponseCode.NOT_FOUND)

    def postFile(request: Request, s: WebServer) -> Response:
        print("postfile")
        expected_file = request.path_components[1]
        with open(os.path.join(s.file_directory, expected_file), "w") as f:
            f.write(request.body)
        return Response(ResponseCode.CREATED)
        