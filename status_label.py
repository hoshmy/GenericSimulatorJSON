from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import pyqtSlot

from ninja_widget import NinjaWidget
from utilities import Utilities
from global_declarations import EntityNameMorphology


class StatusLabel(QLabel, NinjaWidget):

    def __init__(self, entity_data, parent=None):
        self._status_data = entity_data
        widget_name = self._parse_widget_name(self._status_data[EntityNameMorphology.ENTITY_NAME.value])
        QLabel.__init__(self, widget_name=widget_name)
        NinjaWidget.__init__(self, widget_name=widget_name)

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
