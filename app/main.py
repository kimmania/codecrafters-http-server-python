import socket
from .request import Request, RequestMethod
from .response import Response, StatusCode

Max_BUFFER_SIZE = 1024
 
def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=False)
    (conn, addr) = server_socket.accept() # wait for client
    
    with conn:
        print(f'addr: {addr}')
        data = conn.recv(Max_BUFFER_SIZE).decode()
        request = Request(data, conn)

        if request.method == RequestMethod.GET:
            get(request)
        else:
            pass

def get(request: Request) -> None:
    if request.target == "/":
        request.respond(Response(StatusCode.OK))
    else:
        request.respond(Response(StatusCode.NOT_FOUND))

if __name__ == "__main__":
    main()
