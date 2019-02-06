import argparse
from src.http import Http
import sys


class Core:
    def __init__(self):
        self.args = None
        self.parser = argparse.ArgumentParser(
            description='httpc is a curl-like application but supports HTTP protocol only.')
        self.parser.add_argument('method',
                                 choices=['get', 'post'],
                                 help='Method')
        self.parser.add_argument('url', type=str)
        self.parser.add_argument('-d', help='Associates an inline data to the body HTTP POST request.', type=str)
        self.parser.add_argument('-e', help='Associates headers to HTTP Request with the format\'key:value\'.',
                                 action='append')
        self.parser.add_argument('-v', help='Prints the detail of the response such as protocol, status,and headers.',
                                 action='store_true')

    def run(self):
        self.args = self.parser.parse_args(sys.argv[1:])
        args = self.args
        http = Http(args.url)
        if args.method == 'get':
            resp = http.get(headers=args.e)
        else:
            resp = http.post(data=args.d, headers=args.e)
        if args.v:
            self.print_details(resp)

        sys.stdout.write(str(resp.body, encoding='utf-8'))
        # print(str(resp.body, encoding='utf-8'), end='')

    def print_details(self, resp):
        print(f"< HTTP/{resp.version} {resp.status} {resp.code}")
        for (value, key) in resp.headers.items():
            print(f"< {value}: {key}")
