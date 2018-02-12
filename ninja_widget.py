import os

class NinjaWidget():
    def __init__(self, widget_name):
        self._widget_name = widget_name

    def _parse_widget_name(self, widget_file_path):
        file_name_without_path =  widget_file_path.split('/')[-1]
        file_name_without_extention = file_name_without_path.split('.')[0]
        return file_name_without_extention

    def _is_widget_file_exists(self,widget_file_path):
        return os.path.isfile(widget_file_path)

    def _log(self, message):
        print('{}: {}'.format(self._widget_name, message))