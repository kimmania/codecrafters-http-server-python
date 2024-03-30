import socket
from .request import Request, RequestMethod
from .response import Response, ResponseCode

def processRequest(conn: socket):
    with conn:
        try:
            request = Request(conn)
        except ValueError:
            print("Exception, sending bad request")
            Response(ResponseCode.BAD_REQUEST).send(conn)
            return # exit

        try:
            match request.header.method:
                case RequestMethod.GET:
                    get(request)
                case _:
                    # handle when we get a method that we are not processing yet
                    Response(ResponseCode.METHOD_NOT_ALLOWED).send(conn)
        except:
            # failed to process, indicate a server error
            Response(ResponseCode.INTERNAL_SERVER_ERROR).send(conn)
            return

def get(request: Request) -> None:
    print(f'path: {request.path()}')
    match request.path():
        case "/":
            request.status(ResponseCode.OK).end()
        case "/user-agent":
            request.status(ResponseCode.OK).text(request.getHeaderValue("user-agent")).end()
        case path if path.startswith("/echo/"):
            request.status(ResponseCode.OK).text(path.removeprefix("/echo/")).end()
        case _:
            request.status(ResponseCode.NOT_FOUND).end()
