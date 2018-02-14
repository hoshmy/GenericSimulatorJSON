from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot

from ninja_widget import NinjaWidget
from communcation import instance as communication
# from scheduler import instance as scheduler


class StatusLabel(QLabel, NinjaWidget):

    def __init__(self, status_file_name, parent=None):
        widget_name = self._parse_widget_name(status_file_name)
        QLabel.__init__(self, widget_name=widget_name)
        NinjaWidget.__init__(self, widget_name=widget_name)

        self._status_file_name = status_file_name
        self._status_data = self._widget_name
        self.setText(self._widget_name)

        self._init_connections()

    def _init_connections(self):
        pass
        # scheduler.signal_heartbeat.connect(self.slot_incoming_status)

    @pyqtSlot(int)
    def _slot_heartbeat(self, heartbeat_index):
        self.setText(self._status_data + str(heartbeat_index))

    @pyqtSlot('QString')
    def slot_incoming_status(self, message):
        self._status_data = message