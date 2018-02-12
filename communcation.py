from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QObject


class Communication(QObject):
    def __init__(self, parent=None):
        QObject.__init__(self, parent)
        self._message_id = 1

    def _init_communication(self):
        pass

    @pyqtSlot('QString')
    def send(self, message):
        self._log('sending {}'.format(message))

    def _log(self, message):
        print('{}: {}'.format('communication', message))

instance = Communication()