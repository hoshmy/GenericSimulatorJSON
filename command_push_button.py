from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import pyqtSignal

from ninja_widget import NinjaWidget
from communcation import instance as communication
from global_declarations import EntityNameMorphology

class CommandPushButton(QPushButton, NinjaWidget):

    _signal_send_via_communication = pyqtSignal('QString')

    def __init__(self, entity_data):
        self._status_data = entity_data
        widget_name = self._parse_widget_name(self._status_data[EntityNameMorphology.ENTITY_NAME.value])
        QPushButton.__init__(self, widget_name=widget_name)
        NinjaWidget.__init__(self, widget_name=widget_name)

        self._command_data = entity_data
        self.setText(self._widget_name)

        self._init_connections()

    def _init_connections(self):
        self.released.connect(self._clicked)

        self._signal_send_via_communication.connect(communication.send)

    def _parse_command(self):
        command_file_name = self._command_data[EntityNameMorphology.ENTITY_FOLDER.value]
        command = ''
        if self._is_widget_file_exists(command_file_name):
            with open(command_file_name, mode='r') as f:
                command = f.read()
        else:
            self._log('widget file {} does\'nt exists'.format(command_file_name))

        return command

    def _send_command(self, command):
        self._log('sending: {}'.format(command))
        self._signal_send_via_communication.emit(command)

    def _clicked(self, bool=False):
        self._log('released')
        command = self._parse_command()
        if command:
            self._send_command(self._parse_command())
        else:
            self._log('command is empty')




