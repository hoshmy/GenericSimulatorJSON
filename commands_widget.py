from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGridLayout
import os

from ninja_widget import NinjaWidget
from command_push_button import CommandPushButton
from utilities import Utilities

class CommandsWidget(QWidget, NinjaWidget):

    def __init__(self, commands_folder, parent=None):
        widget_name = self._parse_widget_name(commands_folder)
        QWidget.__init__(self, widget_name=widget_name, parent=parent)
        NinjaWidget.__init__(self, widget_name=widget_name)

        self._commands_folder = commands_folder
        self._build_ui()
        self._init_connections()

    def _init_connections(self):
        pass

    def _build_ui(self):
        grid_layout = QGridLayout(self)
        self.setLayout(grid_layout)

        # title = QLabel("{}".format(self._widget_name), self)
        # title.setAlignment(QtCore.Qt.AlignCenter)
        #
        # grid_layout.addWidget(title, 0, 0)

        if os.path.exists(self._commands_folder):
            for root, dirs, files in os.walk(self._commands_folder):
                for i, file in enumerate(files):
                    current_button_file_name = os.path.join(self._commands_folder, file)
                    current_button = CommandPushButton(command_file_name=current_button_file_name)
                    row = Utilities.calculate_row(i)
                    col = Utilities.calculate_column(i)
                    grid_layout.addWidget(current_button, col, row)

