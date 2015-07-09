#! /usr/bin/env python

from dataprovider import DataProvider
import time
import SocketServer

class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        data = DataProvider()
        while True:
            try:
                self.request.send(data.getData())
            except:
                # Client closed/lost connection
                break
            time.sleep(1.0/25.0)


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    server = SocketServer.ThreadingTCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()

