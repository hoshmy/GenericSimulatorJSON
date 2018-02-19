from enum import Enum


class EntityNameMorphology(Enum):
        LOCATION_INDEX = 0
        ENTITY_TYPE = 1
        ENTITY_NAME = 2
        ENTITY_FOLDER = 3
        ENTITY_SHOULD_DISPLAY = 4
        ENTITY_DATA_SIZE = 5


class EntityType(Enum):
    ENTITY_TYPE_COMMAND = 'command'
    ENTITY_TYPE_STATUS = 'status'
    ENTITY_TYPE_MIXED = 'mixed'
    ENTITY_TYPE_BOOLEAN = 'boolean'


class General(Enum):
    WINDOW_HEIGHT = 300
    WINDOW_WIDTH = 1000
    MAX_WIDGETS_COLUMN_HEIGHT = 7
    UDP_IP = "127.0.0.1"
    UDP_PORT = 5005
    RESOURCES_FOLDER = 'resources'
    LOGO_NAME = 'logo.jpeg'

    LOGO_HEIGHT = 205
    LOGO_WIDTH = 144
    MIXED_TAB_GRID_LAYOUT_MINIMUM_WIDTH = WINDOW_WIDTH - LOGO_WIDTH - 50
    STATUS_LABEL_MAXIMUM_HEIGHT = 15


class StatusBehaviourKey(Enum):
        LABEL_TEXT = 'label_text'
        STATUS_FROM_COMMUNICATION = 'status_from_communication'
        PATH_IN_MESSAGE = 'path_in_message'


