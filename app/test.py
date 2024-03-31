from request import Request


temp = "GET / HTTP/1.1\r\nHost: localhost:4221\r\nUser-Agent: Go-http-client/1.1\r\nAccept-Encoding: gzip\r\n"

request = Request(temp)