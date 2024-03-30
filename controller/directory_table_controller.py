from datetime import datetime
from pathlib import Path
from PyQt6.QtGui import QStandardItemModel, QStandardItem

import utils


class DirectoryTableController:
    def __init__(self, main_view):
        self.table_model = QStandardItemModel(0, 5)
        self.table_model.setHorizontalHeaderLabels(['Name', 'Date Modified', 'Type', 'Size', 'Path'])
        self.main_view = main_view


    def navigate_to_link(self):
        row = self.main_view.tree_view.selectionModel().currentIndex().row()
        item = self.table_model.item(row, 4)
        print(item.text())
        path = item.text()

        path_obj = Path(path)
        if path and path_obj.is_dir():
            # self.search_directory_content(path)
            pass # reference

    def search_directory_contents(self, path):
        # clear previous records (if any)
        self.table_model.removeRows(0, self.table_model.rowCount())
        # populate table
        path_obj = Path(path)
        print(str(path_obj.parent))

        for file in path_obj.iterdir():
            file_info = file.stat()
            name = file.name
            size = str(utils.get_file_size_in_kb(file_info.st_size)) if file.is_file() else " "
            date = datetime.fromtimestamp(file_info.st_mtime).strftime('%d/%m/%Y %H:%M')
            file_type = Path(file.name).suffix if file.is_file() else "File Folder"
            path = str(file)
            item_list = [QStandardItem(name), QStandardItem(date), QStandardItem(file_type),
                         QStandardItem(size), QStandardItem(path)]
            self.table_model.appendRow(item_list)
        self.main_view.table_view.setModel(self.table_model)


