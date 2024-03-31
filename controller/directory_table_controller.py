import os
from datetime import datetime
from pathlib import Path
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QMessageBox

import utils
from view.error_message import ErrorMessageBox

# manages QTableView in main view
# has reference to QStandardItemModel that handles and displays files in directories
# has reference to the main_view
class DirectoryTableController:
    def __init__(self, main_view):
        self.table_model = QStandardItemModel(0, 5)
        self.table_model.setHorizontalHeaderLabels(['Name', 'Date Modified', 'Type', 'Size', 'Path'])
        self.main_view = main_view
        self.search_directory_contents(os.path.expanduser('~'))


    # def navigate_to_link(self):
    #     row = self.main_view.tree_view.selectionModel().currentIndex().row()
    #     item = self.table_model.item(row, 4)
    #     print(item.text())
    #     path = item.text()
    #
    #     path_obj = Path(path)
    #     if path and path_obj.is_dir():
    #         # self.search_directory_content(path)
    #         pass # reference

    def search_directory_contents(self, path):
        try:
            # clear previous records (if any)
            init_row_count = self.table_model.rowCount()
            # self.table_model.removeRows(0, init_row_count)

            # populate table
            path_obj = Path(path)
            print(str(path_obj.parent))
            for file in path_obj.iterdir():
                # do not add to table if not accessible
                if os.access(file, os.R_OK):
                    file_info = file.stat()
                    name = str(file.name)
                    size = str(utils.get_file_size_in_kb(file_info.st_size)) if file.is_file() else " "
                    # avoid converting negative file_info.st_mtime timestamps because os error
                    date = datetime.fromtimestamp(file_info.st_mtime).strftime('%d/%m/%Y %H:%M') if file_info.st_mtime >= 0 else ""
                    file_type = Path(file.name).suffix if file.is_file() else "File Folder"
                    path = str(file)
                    item_list = [QStandardItem(name), QStandardItem(date), QStandardItem(file_type),
                                 QStandardItem(size), QStandardItem(path)]
                    # add to table
                    self.table_model.appendRow(item_list)

            # clear all original data (if any new files failed to load, data will remain)
            self.table_model.removeRows(0, init_row_count)

            self.main_view.table_view.setModel(self.table_model)
            self.main_view.table_view.setColumnHidden(4, True)  # hide path column
            self.main_view.table_view.setColumnWidth(0, 300)  # set name col width
            self.main_view.table_view.setColumnWidth(1, 120)  # set name col width
            self.main_view.table_view.setColumnWidth(2, 80)  # set type col width
            self.main_view.table_view.setColumnWidth(3, 80)  # set size col width

        except OSError as e:
            print("os: " + str(e))
            ErrorMessageBox("OS Error", path, str(e))
            return

        except Exception as e:
            print("except: " + str(e))
            ErrorMessageBox("Windows Error", str(e))
            return




