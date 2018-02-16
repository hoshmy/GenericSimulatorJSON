import os

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QSize
from PyQt5.QtCore import Qt

from ninja_widget import NinjaWidget
from command_push_button import CommandPushButton
from status_label import StatusLabel
from global_declarations import EntityType
from global_declarations import EntityNameMorphology
from global_declarations import General
from utilities import Utilities


class MixedTabWidget(QWidget, NinjaWidget):
    def _build_ui(self):
        horizontal_layout = QHBoxLayout()
        self.setLayout(horizontal_layout)

        grid_layout = QGridLayout(self)

        if os.path.exists(self._mixed_tab_folder):
            for root, dirs, files in os.walk(self._mixed_tab_folder):
                for i, file in enumerate(files):
                    entity_data = Utilities.entity_name_break_down(
                            entity_name=file, entity_path=self._mixed_tab_folder
                    )

                    if not Utilities.entity_for_display(entity_data):
                        continue

                    entity_type = entity_data[EntityNameMorphology.ENTITY_TYPE.value]
                    entity = None
                    if entity_type == EntityType.ENTITY_TYPE_COMMAND.value:
                        entity = CommandPushButton(
                            entity_data=entity_data
                        )
                    elif entity_type == EntityType.ENTITY_TYPE_STATUS.value:
                        entity = StatusLabel(
                            entity_data=entity_data
                        )
                    else:
                        self._log('mixed type widget encountered with error entity tpr: {}'.format(entity_data))

                    row = Utilities.calculate_row(i)
                    col = Utilities.calculate_column(i)
                    grid_layout.addWidget(entity, col, row)

        logo_label = QLabel()
        logo_label.setMaximumWidth(General.LOGO_WIDTH.value)
        logo_label.setMaximumHeight(General.LOGO_HEIGHT.value)
        logo_path = os.path.join(General.RESOURCES_FOLDER.value, General.LOGO_NAME.value)
        logo = QPixmap(logo_path)
        logo.scaled(logo_label.size(), Qt.IgnoreAspectRatio)
        logo_label.setPixmap(logo)
        logo_label.setScaledContents(True)

        # Order is important
        horizontal_layout.addWidget(logo_label)
        horizontal_layout.addLayout(grid_layout)




    def __init__(self, mixed_tab_folder, parent=None):
        widget_name = self._parse_widget_name(mixed_tab_folder)
        QWidget.__init__(self, widget_name=widget_name, parent=parent)
        NinjaWidget.__init__(self, widget_name=widget_name)

        self._mixed_tab_folder = mixed_tab_folder

        self._build_ui()
        self._init_connections()
    def _init_connections(self):
        pass
