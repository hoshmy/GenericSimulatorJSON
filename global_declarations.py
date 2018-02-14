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


class General(Enum):
    MAX_WIDGETS_COLUMN_HEIGHT = 2

