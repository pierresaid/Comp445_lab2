# import logging
#
# from src.Core import Core
#
# logging.basicConfig(format='httpc: %(message)s', level=logging.DEBUG)
#
# core = Core()
# try:
#     core.run()
# except Exception as e:
#     logging.error(e)
# exit(0)

from src.http import Http

http = Http()
http.run()

