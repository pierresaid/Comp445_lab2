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
            except:
                break
        print("je close la socket")
        s.shutdown(socket.SHUT_RDWR)
        s.close()

    def process(self, conn):
        result = b''
        new_res = None
        while result.find(b'\r\n\r\n') == -1 and (new_res is None or len(new_res) != 0):
            new_res = conn.recv(1)
            result += new_res
        res = re.findall(b"(GET|POST) (.*) HTTP", result)
        if res[0][0] == b'GET':
            self.Get(str(res[0][1], encoding='utf-8'))
        if res[0][0] == b'POST':
            self.Post()

    def Get(self, path):
        print(f"c un get {path}")

        # print(query)

    def Post(self):
        print("c un post")

# def __init__(self, url):
#     parsed_url = urlparse(url)
#     self.socket = None
#     if parsed_url.path == url:
#         url = "http://" + url
#         parsed_url = urlparse(url)
#     if parsed_url.hostname is None or parsed_url.path is None:
#         raise Exception('<url> malformed')
#     self.hostname = parsed_url.hostname
#     self.path = parsed_url.path
#     if parsed_url.query is not '':
#         self.path += "?" + parsed_url.query
#     if self.path == '':
#         self.path = '/'
#     if parsed_url.port is None:
#         self.port = 80
#     else:
#         self.port = parsed_url.port
#     # print(self.path)
#     # print(self.hostname)
#
# def get(self, headers=None):
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     self.socket = s
#     try:
#         s.connect((self.hostname, self.port))
#     except socket.error:
#         raise Exception(f"Could not resolve host: {self.hostname}")
#
#     query = "GET {0} HTTP/1.1\r\nHost: {1}\r\n".format(self.path, self.hostname)
#     if headers is not None:
#         for h in headers:
#             if re.search("(.+):(.+)", h):
#                 query += h + "\r\n"
#     query += "\r\n\r\n"
#     # print(query)
#     s.sendall(str.encode(query))
#     result = self.read_result()
#     # print(str(result, encoding='utf-8'), end='')
#     s.close()
#     return result
#
# def post(self, data=None, headers=None):
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     self.socket = s
#     s.connect((self.hostname, self.port))
#
#     query = "POST {0} HTTP/1.1\r\nHost: {1}\r\n".format(self.path, self.hostname)
#     if headers is not None:
#         for h in headers:
#             if re.search("(.+):(.+)", h):
#                 query += h + "\r\n"
#     if data is not None:
#         query += "Content-Length: {0}\r\n".format(len(data))
#
#     query += "\r\n"
#     s.sendall(str.encode(query))
#     if data is not None and len(data) > 0:
#         s.sendall(data.encode())
#
#     result = self.read_result()
#     # print(str(result, encoding='utf-8'), end='')
#     s.close()
#     return result
#
# def read_result(self):
#     resp = Response()
#     result = b''
#     new_res = None
#     while result.find(b'\r\n\r\n') == -1 and (new_res is None or len(new_res) != 0):
#         new_res = self.socket.recv(1)
#         result += new_res
#     begin_length_idx = result.find(b'Content-Length: ') + len('Content-Length: ')
#     if begin_length_idx is 15:
#         raise Exception("HTTP version not supported")
#     end_lenght_idx = result[begin_length_idx:].find(b'\r\n')
#     content_length = int(str(result[begin_length_idx:][:end_lenght_idx], encoding='utf-8'))
#     headers = self.get_headers(result)
#     self.get_code_and_status(resp, result)
#     body = self.socket.recv(content_length)
#     resp.headers = headers
#     resp.body = body
#     return resp
#
# def get_headers(self, result):
#     reg = re.findall("(?P<key>.*?):\ +(?P<value>.*?)(?:(\\r\\n){1})", str(result, encoding='utf-8'))
#     reg = [r[:-1] for r in reg]
#     headers = {}
#     for (h) in reg:
#         headers[h[0]] = ''.join(h[1:])
#     return headers
#
# def get_code_and_status(self, resp, result):
#     reg = re.findall("HTTP(.*?)(\\r\\n)", str(result, encoding='utf-8'))
#     reg2 = re.findall("/(.+)\ +(\d\d\d)\ (.+)", reg[0][0])
#     resp.version = reg2[0][0]
#     resp.status = reg2[0][1]
#     resp.code = reg2[0][2]
