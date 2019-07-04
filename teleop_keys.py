import curses
from threading import Thread, Lock
from time import sleep

from behaviour import Behaviour
from motion_command import MotionCommand


class TeleopKeysThread(Thread):
    def __init__(self, screen):
        super().__init__()
        self._run = False
        self._screen = screen
        self._command = MotionCommand()
        self._lock = Lock()

    def run(self):
        self._run = True
        while self._run:
            in_char = self._screen.getch()
            if in_char == curses.KEY_UP:
                with self._lock:
                    self._command.velocity = 0.2
                    self._command.rotation = 0.0
            elif in_char == curses.KEY_DOWN:
                with self._lock:
                    self._command.velocity = -0.2
                    self._command.rotation = 0.0
            elif in_char == curses.KEY_RIGHT:
                with self._lock:
                    self._command.velocity = 0.0
                    self._command.rotation = -1.5
            elif in_char == curses.KEY_LEFT:
                with self._lock:
                    self._command.velocity = 0.0
                    self._command.rotation = 1.5
            elif in_char == 10:
                with self._lock:
                    self._command.velocity = 0.0
                    self._command.rotation = 0.0
            sleep(0.01)

    def stop(self):
        self._run = False
        self.join()

    def get_command(self):
        with self._lock:
            return self._command


class TeleopKeys(Behaviour):
    """
    Teleop behaviour. Remote control the robot.
    """
    def __init__(self, priority):
        super(TeleopKeys, self).__init__(priority, "teleop_keys")
        # Get the curses window, turn off echoing of keyboard to screen, turn on
        # instant (no waiting) key response, and use special values for cursor keys
        self._screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        # Don't block on getch
        self._screen.nodelay(True)
        self._screen.keypad(True)
        self._key_thread = TeleopKeysThread(self._screen)
        self._key_thread.start()

    def stop(self):
        try:
            self._key_thread.stop()
        finally:
            # Close down curses properly, inc turn echo back on!
            curses.nocbreak()
            self._screen.keypad(0)
            curses.echo()
            curses.endwin()
            print('TeleopKeys stopped')

    def get_action(self, sensors=None):
        return self._key_thread.get_command()

    def winner(self, winner=False):
        pass
