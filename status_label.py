from enum import Enum
import json

from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt

from ninja_widget import NinjaWidget
from utilities import Utilities
from global_declarations import EntityNameMorphology
from communcation import instance as communication_instance
from global_declarations import General


class _StatusBehaviourKey(Enum):
        LABEL_TEXT = 'label_text'
        STATUS_FROM_COMMUNICATION = 'status_from_communication'
        PATH_IN_MESSAGE = 'path_in_message'


class StatusLabel(QLabel, NinjaWidget):

    def __init__(self, entity_data, parent=None):
        self._status_data = entity_data
        widget_name = self._parse_widget_name(self._status_data[EntityNameMorphology.ENTITY_NAME.value])
        QLabel.__init__(self, widget_name=widget_name)
        NinjaWidget.__init__(self, widget_name=widget_name)

        self._status_behaviour = {}
        self._current_status = 'N/A'
        self._status_message_from_communication = {}

        self._parse_status_behaviour()
        self._set_style()

        self.setText(self._construct_status_text())
        self._init_connections()

    def _init_connections(self):
        communication_instance.signal_status_update.connect(self.slot_incoming_status)

    def _set_style(self):
        self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.setFrameShape(QFrame.Panel)
        self.setFrameShadow(QFrame.Sunken)
        self.setLineWidth(2)
        self.setMaximumHeight(General.MIXED_TAB_GRID_LAYOUT_MINIMUM_WIDTH.value)

    def _parse_status_behaviour(self):
        status_behaviour_str = {}
        with open(self._status_data[EntityNameMorphology.ENTITY_FOLDER.value], 'r') as file:
            status_behaviour_str = file.read()
        try:
            self._status_behaviour = eval(status_behaviour_str)
        except Exception as e:
            self._log('eval failed with: {}'.format(status_behaviour_str))

    def _construct_status_text(self):
        status_text = ''.join([self._status_behaviour['label_text'], ': ', str(self._current_status)])
        return status_text

    @pyqtSlot(int)
    def _slot_heartbeat(self, heartbeat_index):
        self.setText(self._construct_status_text())

    @pyqtSlot('QString')
    def slot_incoming_status(self, message):
        received_json = json.loads(message)
        self._status_message_from_communication = received_json

        try:
            required_status = self._status_behaviour[_StatusBehaviourKey.STATUS_FROM_COMMUNICATION.value]
            if self._status_message_from_communication['status'] == required_status:
                first_key = self._status_behaviour[_StatusBehaviourKey.PATH_IN_MESSAGE.value][0]
                compliment_keys = self._status_behaviour[_StatusBehaviourKey.PATH_IN_MESSAGE.value][1:]

                # Extract keys
                status = self._status_message_from_communication[first_key]
                for key in compliment_keys:
                    status = status[key]

                self._current_status = status
                self._slot_heartbeat(777)
        except Exception as e:
            self._log('Path in message  wasn\'t correct is {}, Error was {}'.format(
                    self._status_behaviour[EntityNameMorphology.ENTITY_FOLDER.value],
                    str(e)
                )
            )
        self.setText(self._construct_status_text())
