import socket
from .request import Request, RequestMethod
from .response import Response, ResponseCode

Max_BUFFER_SIZE = 1024
 
def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=False)

    while True:
        (conn, addr) = server_socket.accept() # wait for client
        with conn:
            data = conn.recv(Max_BUFFER_SIZE).decode()
            try:
                request = Request(data, conn)
            except ValueError:
                print("Exception, sending bad request")
                Response(ResponseCode.BAD_REQUEST).send(conn)
                continue

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
                continue


def get(request: Request) -> None:
    match request.path():
        case "/":
            request.status(ResponseCode.OK).end()
        case path if path.startswith("/echo/"):
            request.status(ResponseCode.OK).text(path.removeprefix("/echo/")).end()
        case _:
            request.status(ResponseCode.NOT_FOUND).end()

if __name__ == "__main__":
    main()
