import jsonpickle
import socket
import time
from threading import Thread, Lock

from sensors.mock_pose_sensor import MockPoseSensor
from sensors.sensors import Sensors


class Server(Thread):
    def __init__(self, host='localhost', port=0):
        super().__init__()
        self.host = host
        self.port = port
        self._run = False
        self.conn = None
        self._sensors = None
        self._lock = Lock()
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

    def update(self, sensors):
        with self._lock:
            self._sensors = sensors


if __name__ == '__main__':
    server = Server(host='localhost', port=65432)
    server.start()
    mock_pose_sensor = MockPoseSensor()
    sensors = Sensors(sensors=[mock_pose_sensor])
    count = 0
    try:
        while True:
            sensor_readings = sensors.read_sensors()
            server.update(sensor_readings)
            time.sleep(1)
            count = count + 1
            if count > 10:
                count = 0
                mock_pose_sensor.reset()
    except KeyboardInterrupt:
        server.stop()
