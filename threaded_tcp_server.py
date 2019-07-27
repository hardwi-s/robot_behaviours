import socketserver
import time
from threading import Thread, current_thread


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = str(self.request.recv(1024), 'ascii')
        cur_thread = current_thread()
        response = bytes("{}: {}".format(cur_thread.name, data), 'ascii')
        self.request.sendall(response)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class Server:
    def __init__(self, host='localhost', port=0):
        self.server = ThreadedTCPServer((host, port), ThreadedTCPRequestHandler)
        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        server_thread = Thread(target=self.server.serve_forever)
        # Exit the server thread when the main thread terminates
        server_thread.daemon = True
        server_thread.start()

    def stop(self):
        self.server.shutdown()
        self.server.server_close()


def main():
    server = Server(host='localhost', port=65432)
    try:
        while True:
            print('zzz')
            time.sleep(1)
    except KeyboardInterrupt:
        print('Interrupted')
        server.stop()
    print('Exiting')


if __name__ == "__main__":
    main()
