import os
import socket
from urllib.parse import urlparse
import re


class Response:
    def __init__(self):
        self.headers = None
        self.body = None
        self.code = -1
        self.status = ''
        self.version = ''
        self.socket = None


class Http:
    def __init__(self, directory='./'):
        self.conn = None
        self.directory = os.path.realpath(directory)

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("127.0.0.1", 8080))
        s.listen()
        while True:
            try:
                conn, addr = s.accept()
                self.process(conn)
                print("je close la conn")
                conn.close()
            except KeyboardInterrupt:
                break
        print("je close la socket")
        s.shutdown(socket.SHUT_RDWR)
        s.close()

    def process(self, conn):
        self.conn = conn
        result = b''
        new_res = None
        while result.find(b'\r\n\r\n') == -1 and (new_res is None or len(new_res) != 0):
            new_res = conn.recv(1)
            result += new_res
        res = re.findall(b"(GET|POST) /(.*) HTTP", result)
        path = os.path.normpath(str(res[0][1], encoding='utf-8'))
        if res[0][0] == b'GET':
            self.Get(path)
        if res[0][0] == b'POST':
            self.Post(path)

    def Get(self, path):
        print(f"c un get {path}")
        try:
            f = open(f"{path}", "r")
        except (FileNotFoundError, IsADirectoryError):
            self.Responde(404, "NOT FOUND")
            return
        self.Responde(200, "OK", f.read())

    def Post(self, path):
        try:
            f = open(f"{path}", "rw")
        except (FileNotFoundError, IsADirectoryError):
            self.Responde(404, "NOT FOUND")
            return
        self.Responde(200, "OK")
        print("c un post")

    def Responde(self, code, status, data=None):
        if data is not None:
            query = f"HTTP/1.1 {code} {status}\r\nContent-Length: {len(data)}\r\n\r\n{data}"
        else:
            query = f"HTTP/1.1 {code} {status}\r\nContent-Length: 0\r\n\r\n"
        self.conn.sendall(str.encode(query))
