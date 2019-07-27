import socket
import time
from threading import Thread


class Server(Thread):
    def __init__(self, host='localhost', port=0):
        super().__init__()
        self.host = host
        self.port = port
        self._run = False
        self.conn = None
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))

    def run(self):
        self._run = True
        while self._run:
            self.socket.listen(1)
            print('Listening on port ' + str(self.port))
            try:
                self.conn, addr = self.socket.accept()
                with self.conn:
                    print('Connection from', addr)
                    while self._run:
                        data = self.conn.recv(1024)
                        if data:
                            self.conn.sendall(data)
                        else:
                            break
                self.conn = None
            except OSError:
                print('Interrupted')

        self.socket.close()

    def stop(self):
        self._run = False
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
        if self.conn:
            try:
                self.conn.shutdown(socket.SHUT_RDWR)
                self.conn.close()
            except OSError:
                pass
        self.join()


if __name__ == '__main__':
    server = Server(host='localhost', port=65432)
    server.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        server.stop()
