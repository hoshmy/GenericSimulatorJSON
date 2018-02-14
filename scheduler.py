from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal
import time
from threading import Thread


class Scheduler(QObject):

    _heartbeat_cycle_time_seconds = 1
    signal_heartbeat = pyqtSignal(int)

    def __init__(self, parent=None):
        QObject.__init__(self, parent)
        self._keep_running = True
        self._heartbeat_counter = 0
        self._running_thread = Thread(target=self._run())
        self._running_thread.start()

    def _run(self):
        starting_time = time.time()
        while self._keep_running:
            starting_time = time.time()

            self.signal_heartbeat.emit(self._heartbeat_counter)

            delta_time = time.time() - starting_time
            sleep_time = Scheduler._heartbeat_cycle_time_seconds - delta_time
            if sleep_time > 0:
                time.sleep(sleep_time)

    def _log(self, message):
        print('{}: {}'.format('Scheduler', message))


# instance = Scheduler()