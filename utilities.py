import os

from global_declarations import EntityNameMorphology
from global_declarations import General


class Utilities:

    @staticmethod
    def entity_name_break_down(entity_name, entity_path):
        # break 01_type_my_name to ['01', 'type', 'my name']

        current_entity_data = [''] * EntityNameMorphology.ENTITY_DATA_SIZE.value

        split_entity_name = entity_name.split('_')
        current_entity_nice_name = ' '.join(split_entity_name[EntityNameMorphology.ENTITY_NAME.value:])
        current_entity_data[EntityNameMorphology.ENTITY_NAME.value] = current_entity_nice_name
        current_entity_data[EntityNameMorphology.LOCATION_INDEX.value] = \
            split_entity_name[EntityNameMorphology.LOCATION_INDEX.value]
        current_entity_data[EntityNameMorphology.ENTITY_FOLDER.value] = os.path.join(entity_path, entity_name)
        current_entity_data[EntityNameMorphology.ENTITY_TYPE.value] = \
            split_entity_name[EntityNameMorphology.ENTITY_TYPE.value]
        current_entity_data[EntityNameMorphology.ENTITY_SHOULD_DISPLAY.value] = not entity_name.endswith('-')

        return current_entity_data

    @staticmethod
    def entity_for_display(entity_data):
        return entity_data[EntityNameMorphology.ENTITY_SHOULD_DISPLAY.value]

    @staticmethod
    def calculate_row(index_location):
        return int(index_location/General.MAX_WIDGETS_COLUMN_HEIGHT.value)

    @staticmethod
    def calculate_column(index_location):
        return index_location%General.MAX_WIDGETS_COLUMN_HEIGHT.value


if __name__ == '__main__':
    print(Utilities.entity_name_break_down('01_type_my_name', 'tabs'))
