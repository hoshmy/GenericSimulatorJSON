import os
from enum import Enum

from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QWidget

from ninja_widget import NinjaWidget
from commands_widget import CommandsWidget
from statuses_widget import StatusesWidget
from mixed_tab_widget import MixedTabWidget
from global_declarations import EntityNameMorphology
from utilities import Utilities
from global_declarations import EntityType


class FoldersBasedTabWidget(QTabWidget, NinjaWidget):

    def __init__(self, tabs_folder, parent=None):
        QTabWidget.__init__(self, widget_name=self._parse_widget_name(tabs_folder), parent=parent)
        NinjaWidget.__init__(self, widget_name=self._parse_widget_name(tabs_folder))

        self._tabs_data = self._parse_tabs_names(tabs_folder)
        self._build_tabs()
        self._init_connections()

    def _build_tabs(self):
        for tab_data in self._tabs_data:
            if Utilities.entity_for_display(tab_data):
                tab_name = tab_data[EntityNameMorphology.ENTITY_NAME.value]
                widget = QWidget(self)
                tab = self.addTab(widget, tab_name)
                self._build_tab(tab_data=tab_data, base_widget=widget)

    def _build_tab(self, tab_data, base_widget):
        tab_type = tab_data[EntityNameMorphology.ENTITY_TYPE.value]
        if EntityType.ENTITY_TYPE_COMMAND.value == tab_type:
            CommandsWidget(
                commands_folder=tab_data[EntityNameMorphology.ENTITY_FOLDER.value],
                parent=base_widget
            )
        elif EntityType.ENTITY_TYPE_STATUS.value == tab_type:
            StatusesWidget(
                statuses_folder=tab_data[EntityNameMorphology.ENTITY_FOLDER.value],
                parent=base_widget
            )
        elif EntityType.ENTITY_TYPE_MIXED.value == tab_type:
            MixedTabWidget(
                mixed_tab_folder=tab_data[EntityNameMorphology.ENTITY_FOLDER.value],
                parent=base_widget
            )
        else:
            self._log('unidentified tab type: {}'.format(tab_type))

    def _parse_tabs_names(self, tabs_folder):
        tabs_data = []
        if os.path.exists(tabs_folder):
            folders_names = os.listdir(tabs_folder)

            for folder_name in folders_names:
                current_tab_data = Utilities.entity_name_break_down(folder_name, tabs_folder)
                tabs_data.append(current_tab_data)
        else:
            self._log('Tabs folder doesnt exists')
        print(tabs_data)
        return tabs_data

    def _init_connections(self):
        pass
