from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import pyqtSignal

from ninja_widget import NinjaWidget
from communcation import instance as communication


class CommandPushButton(QPushButton, NinjaWidget):

    _send_via_communication = pyqtSignal('QString')

    def __init__(self, command_file_name):
        QPushButton.__init__(self, widget_name='')
        NinjaWidget.__init__(self, widget_name=self._parse_widget_name(command_file_name))

        self._command_file_name = command_file_name
        self.setText(self._parse_widget_name(command_file_name))

        # Declare signals
        # self._send_via_communication = pyqtSignal('QString')

        self.init_connections()

    def init_connections(self):
        self.released.connect(self._clicked)

        # communication.send.connect(self._send_via_communication)
        self._send_via_communication.connect(communication.send)

    def _parse_command(self):
        command = ''
        if self._is_widget_file_exists(self._command_file_name):
            with open(self._command_file_name, mode='r') as f:
                command = f.read()
        else:
            self._log('widget file {} does\'nt exists'.format(self._command_file_name))

        return command

    def _send_command(self, command):
        self._log('sending: {}'.format(command))
        self._send_via_communication.emit(command)

    def _clicked(self, bool=False):
        self._log('released')
        command = self._parse_command()
        if command:
            self._send_command(self._parse_command())
        else:
            self._log('command is empty')




