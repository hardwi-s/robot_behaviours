import jsonpickle
import socket
import time
from threading import Thread, Lock

from pose import Pose


class Server(Thread):
    def __init__(self, host='localhost', port=0):
        super().__init__()
        self.host = host
        self.port = port
        self._run = False
        self.conn = None
        self._sensors = None
        self._lock = Lock()
        self._pose=Pose()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))

    def _handle(self, data):
        try:
            in_string = data.decode().rstrip('\r\n')
            if in_string == 'sensors':
                with self._lock:
                    sensors_string = jsonpickle.encode(self._sensors) + '\n'
                    self.conn.sendall(sensors_string.encode('utf-8'))
                    pose_string = jsonpickle.encode(self._pose) + '\n'
                    self.conn.sendall(pose_string.encode('utf-8'))
            else:
                self.conn.sendall(b'unknown\n')
        except UnicodeDecodeError:
            self.conn.sendall(b'error\n')

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
                            self._handle(data)
                        else:
                            print('Connection closed')
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

    def update(self, sensors, pose):
        with self._lock:
            self._sensors = sensors
            self._pose = pose


if __name__ == '__main__':
    server = Server(host='localhost', port=65432)
    server.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        server.stop()
