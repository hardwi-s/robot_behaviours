import time


class Timeout:
    def __init__(self):
        self._end_time = 0

    def start(self, time_sec):
        self._end_time = time.perf_counter() + time_sec

    def is_expired(self):
        if self._end_time <= time.perf_counter():
            return True
        else:
            return False


if __name__ == "__main__":
    timeout = Timeout()
    timeout.start(10)
    i = 0
    while not timeout.is_expired():
        print(i)
        i = i + 1
        time.sleep(1)
    print ('done')
