import os
import socket
import re
from os import listdir
from os.path import isfile, join


class Response:
    def __init__(self):
        self.headers = None
        self.body = None
        self.code = -1
        self.status = ''
        self.version = ''
        self.socket = None


class Http:
    def __init__(self, directory='./', verbose=False, port=8080):
        self.conn = None
        self.directory = os.path.realpath(directory)
        self.verbose = verbose
        self.port = port

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("127.0.0.1", self.port))
        s.listen()
        while True:
            try:
                conn, addr = s.accept()
                self.process(conn)
                conn.close()
            except KeyboardInterrupt:
                break
        s.shutdown(socket.SHUT_RDWR)
        s.close()

    def process(self, conn):
        self.conn = conn
        result = b''
        new_res = None
        while result.find(b'\r\n\r\n') == -1 and (new_res is None or len(new_res) != 0):
            new_res = conn.recv(1)
            result += new_res
        if self.verbose:
            a = str(result, encoding='utf-8').split('\r\n')
            b = [s for s in a if s is not ""]
            for s in b:
                print('< ' + s)
        res = re.findall(b"(GET|POST) /(.*) HTTP", result)

        content_length = None
        data = None
        begin_length_idx = result.find(b'Content-Length: ') + len('Content-Length: ')
        if begin_length_idx is not 15:
            end_lenght_idx = result[begin_length_idx:].find(b'\r\n')
            content_length = int(str(result[begin_length_idx:][:end_lenght_idx], encoding='utf-8'))
        if content_length is not None:
            data = conn.recv(content_length)

        if str(res[0][1], encoding='utf-8') == "":
            self.DefaultGet()
        else:
            path = os.path.normpath(str(res[0][1], encoding='utf-8'))
            # print(self.directory + "/" + path)
            if res[0][0] == b'GET':
                self.Get(self.directory + "/" + path)
            if res[0][0] == b'POST':
                self.Post(self.directory + "/" + path, data)

    def DefaultGet(self):
        onlyfiles = [f for f in listdir(self.directory) if isfile(join(self.directory, f))]
        strfiles = '\n'.join(onlyfiles)
        self.Responde(200, "OK", strfiles + '\n')

    def Get(self, path):
        try:
            f = open(f"{path}", "r")
        except (FileNotFoundError, IsADirectoryError) as err:
            if type(err) is FileNotFoundError:
                self.Responde(404, "NOT FOUND", "File not found.\n")
            else:
                self.Responde(403, "FORBIDDEN", "Trying to read directory.\n")
            return
        self.Responde(200, "OK", f.read())

    def Post(self, path, data):
        try:
            exist = os.path.isfile(path)
            f = open(path, "w+")
        except IsADirectoryError:
            self.Responde(403, "FORBIDDEN", "Cannot write there\n")
            return
        f.write(str(data, encoding='utf-8'))
        if not exist:
            self.Responde(201, "CREATED")
        else:
            self.Responde(200, "OK")

    def Responde(self, code, status, data=None):
        if data is not None:
            query = f"HTTP/1.1 {code} {status}\r\nContent-Length: {len(data)}\r\n\r\n{data}"
        else:
            query = f"HTTP/1.1 {code} {status}\r\nContent-Length: 0\r\n\r\n"
        if self.verbose:
            a = f"HTTP/1.1 {code} {status}\r\nContent-Length: {len(data)}".split('\r\n')
            b = [s for s in a if s is not ""]
            for s in b:
                print('> ' + s)
        self.conn.sendall(str.encode(query))
