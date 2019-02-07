import argparse
from src.http import Http
import sys


class Core:
    def __init__(self):
        self.args = None
        self.parser = argparse.ArgumentParser(
            description='httpfs is a simple file server.')
        self.parser.add_argument('-v', help='Prints debugging messages.',
                                 action='store_true')
        self.parser.add_argument('-p',
                                 help='Specifies the port number that the server will listen and serve at. Default is 8080.',
                                 type=int)
        self.parser.add_argument('-d',
                                 help='Specifies the directory that the server will use to read/write requested files. Default is the current directory when launching the application.',
                                 type=str)

    def run(self):
        self.args = self.parser.parse_args(sys.argv[1:])
        args = self.args
        http = Http(directory=args.d if args.d is not None else "./",
                    verbose=args.v,
                    port=args.p if args.p is not None else 8080)
        http.run()
