from enum import Enum
import json
import os

from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QStackedWidget
from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from ninja_widget import NinjaWidget
from utilities import Utilities
from global_declarations import EntityNameMorphology
from communcation import instance as communication_instance
from global_declarations import General
from global_declarations import StatusBehaviourKey


class _BooleanType(Enum):
    NONE = 0
    ON = 1
    OFF = 2


class _Parameters(Enum):
        RESOURCES_FOLDER = 'label_text'
        STATUS_FROM_COMMUNICATION = 'status_from_communication'
        PATH_IN_MESSAGE = 'path_in_message'
        BOOLEAN_BULB_WIDTH = 30
        BOOLEAN_BULB_HEIGHT = 30
        HEADER_LABEL_WIDTH = 270
        HEADER_LABEL_HEIGHT = 30
        TOTAL_WIDGET_WIDTH = 300
        TOTAL_WIDGET_HEIGHT = 34
        NONE_ICON_NAME = 'question_mark.png'
        TRUE_ICON_NAME = 'true.png'
        FALSE_ICON_NAME = 'false.png'


class BooleanWidget(QWidget, NinjaWidget):

    def __init__(self, entity_data, parent=None):
        self._boolean_data = entity_data
        widget_name = self._parse_widget_name(self._boolean_data[EntityNameMorphology.ENTITY_NAME.value])
        QWidget.__init__(self, widget_name=widget_name)
        NinjaWidget.__init__(self, widget_name=widget_name)

        self._boolean_behaviour = {}
        self._booleans_stacked_widget = None
        self._status_message_from_communication = {}
        self._current_is_on = None
        self._frame = None

        self._parse_status_behaviour()
        self._build_ui()
        self._set_style()
        self._init_connections()

    def _init_connections(self):
        communication_instance.signal_status_update.connect(self._slot_incoming_status)

    def _set_style(self):
        self.setMaximumWidth(_Parameters.TOTAL_WIDGET_WIDTH.value)
        self.setMaximumHeight(_Parameters.TOTAL_WIDGET_HEIGHT.value)
        self._frame.setParent(self)
        self._frame.setStyleSheet('border: 2px solid black;')

    def _parse_status_behaviour(self):
        status_behaviour_str = {}
        with open(self._boolean_data[EntityNameMorphology.ENTITY_FOLDER.value], 'r') as file:
            status_behaviour_str = file.read()
        try:
            self._boolean_behaviour = eval(status_behaviour_str)
        except Exception as e:
            self._log('eval failed with: {}'.format(status_behaviour_str))

    def _build_ui(self):
        # self._frame = QFrame(self)
        self._frame = QFrame()
        self._frame.setStyleSheet('border: 2px solid black;')
        horizontal_layout = QHBoxLayout(self._frame)
        self.setLayout(horizontal_layout)

        self._booleans_stacked_widget = QStackedWidget()
        self._init_booleans_types()

        header_label = QLabel()
        header_label.setText(self._boolean_behaviour[StatusBehaviourKey.LABEL_TEXT.value])
        # header_label.setMaximumWidth(_Parameters.HEADER_LABEL_WIDTH.value)
        # header_label.setMaximumHeight(_Parameters.HEADER_LABEL_HEIGHT.value)

        self._set_boolean_type()

        # Order is important
        horizontal_layout.addWidget(header_label)
        horizontal_layout.addWidget(self._booleans_stacked_widget)

    def _init_booleans_types(self):
        self._init_boolean_type(_BooleanType.NONE.value, _Parameters.NONE_ICON_NAME.value)
        self._init_boolean_type(_BooleanType.ON.value, _Parameters.TRUE_ICON_NAME.value)
        self._init_boolean_type(_BooleanType.OFF.value, _Parameters.FALSE_ICON_NAME.value)

    def _init_boolean_type(self, index, resource_name):
        boolean_label = QLabel()
        boolean_label.setMaximumWidth(_Parameters.BOOLEAN_BULB_WIDTH.value)
        # boolean_label.setMinimumWidth(_Parameters.BOOLEAN_BULB_WIDTH.value)
        boolean_label.setMaximumHeight(_Parameters.BOOLEAN_BULB_HEIGHT.value)
        # boolean_label.setMinimumHeight(_Parameters.BOOLEAN_BULB_HEIGHT.value)
        boolean_path = os.path.join(General.RESOURCES_FOLDER.value, resource_name)
        boolean_pixmap = QPixmap(boolean_path)
        boolean_pixmap.scaled(boolean_label.size(), Qt.KeepAspectRatio)
        boolean_label.setPixmap(boolean_pixmap)
        boolean_label.setScaledContents(True)

        self._booleans_stacked_widget.insertWidget(index, boolean_label)

    def _set_boolean_type(self):
        index = 0
        if self._current_is_on is None:
            index = _BooleanType.NONE.value
        elif self._current_is_on:
            index = _BooleanType.ON.value
        else:
            index = _BooleanType.OFF.value

        self._booleans_stacked_widget.setCurrentIndex(index)

    @pyqtSlot('QString')
    def _slot_incoming_status(self, message):
        received_json = json.loads(message)
        self._status_message_from_communication = received_json

        try:
            required_status = self._boolean_behaviour[StatusBehaviourKey.STATUS_FROM_COMMUNICATION.value]
            if self._status_message_from_communication['status'] == required_status:
                first_key = self._boolean_behaviour[StatusBehaviourKey.PATH_IN_MESSAGE.value][0]
                compliment_keys = self._boolean_behaviour[StatusBehaviourKey.PATH_IN_MESSAGE.value][1:]

                # Extract keys
                status = self._status_message_from_communication[first_key]
                for key in compliment_keys:
                    status = status[key]

                self._current_is_on = bool(status)
                self._set_boolean_type()
        except Exception as e:
            self._log('Path in message  wasn\'t correct is {}, Error was {}'.format(
                    self._boolean_data[EntityNameMorphology.ENTITY_FOLDER.value],
                    str(e)
                )
            )
