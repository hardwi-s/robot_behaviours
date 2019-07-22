import socketserver
import time
from threading import Thread


class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())


class ServerThread(Thread):
    def __init__(self):
        super().__init__()
        HOST, PORT = "localhost", 9999

        # Create the server, binding to localhost on port 9999
        self._server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

    def run(self):
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        self._server.serve_forever()

    def stop(self):
        self._server.shutdown()
        self.join()


def main():
    server = ServerThread()
    try:
        server.start()
        while True:
            print('zzz')
            time.sleep(1)
    except KeyboardInterrupt:
        print('Interrupted')
        server.stop()
    print('Exiting')


if __name__ == "__main__":
    main()
