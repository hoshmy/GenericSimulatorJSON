from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGridLayout
import os

from ninja_widget import NinjaWidget
from status_label import StatusLabel


class StatusesWidget(QWidget, NinjaWidget):

    def __init__(self, statuses_folder, parent=None):
        widget_name = self._parse_widget_name(statuses_folder)
        QWidget.__init__(self, widget_name=widget_name, parent=parent)
        NinjaWidget.__init__(self, widget_name=widget_name)

        self._statuses_folder = statuses_folder
        self._build_ui()
        self._init_connections()

    def _init_connections(self):
        pass

    def _build_ui(self):
        grid_layout = QGridLayout(self)
        self.setLayout(grid_layout)

        # title = QLabel("statuses {}".format(self._widget_name), self)
        # title.setAlignment(QtCore.Qt.AlignCenter)
        #
        # grid_layout.addWidget(title, 0, 0)

        if os.path.exists(self._statuses_folder):
            for root, dirs, files in os.walk(self._statuses_folder):
                for i, file in enumerate(files):
                    current_status_file_name = os.path.join(self._statuses_folder, file)
                    current_label = StatusLabel(current_status_file_name)
                    # current_label = QLabel("{}".format(file), self)
                    grid_layout.addWidget(current_label, i, 0)