from datetime import datetime, timezone
from pathlib import Path
from PyQt6 import uic
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import utils
import subprocess, os, platform

from directory_stack import DirectoryStack


class MyApplication(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI/main.ui", self)
        self.show()

        # load models
        self.tree_model = QFileSystemModel()
        self.file_table_model = QStandardItemModel(0, 5)
        # self.file_table_model.setHorizontalHeaderLabels(['Name', 'Date Modified', 'Type', 'Size', 'Path'])
        self.directory_stack = DirectoryStack(str(Path.home()))

        # get visual elements
        self.browse_button = self.findChild(QPushButton, "browse_file_button")
        self.search_box = self.findChild(QLineEdit, "search_box")
        self.search_box_warning = self.findChild(QLabel, "search_box_warning")
        self.search_result = self.findChild(QTableView, "search_result")
        self.search_tree = self.findChild(QTreeView, "search_tree")
        self.back_button = self.findChild(QPushButton, "back_button")
        self.up_button = self.findChild(QPushButton, "up_button")
        self.next_button = self.findChild(QPushButton, "next_button")

        # config visuals / connect visuals to model
        self.search_result.setModel(self.file_table_model)
        self.load_tree()
        self.load_table_view_settings()
        self.load_button_icons()

        # load interactions
        self.load_click_functions()


    def load_button_icons(self):
        back_icon = QIcon("Icons\\left.png")
        self.back_button.setIcon(back_icon)
        self.back_button.setIconSize(QSize(10, 10))

        up_icon = QIcon("Icons\\up.png")
        self.up_button.setIcon(up_icon)
        self.up_button.setIconSize(QSize(14, 14))

        next_icon = QIcon("Icons\\right.png")
        self.next_button.setIcon(next_icon)
        self.next_button.setIconSize(QSize(12, 12))

    def load_table_view_settings(self):
        self.file_table_model.setHorizontalHeaderLabels(['Name', 'Date Modified', 'Type', 'Size', 'Path'])
        self.search_result.setColumnWidth(0, 300)  # set name col width
        self.search_result.setColumnWidth(2, 80)  # set type col width
        self.search_result.setColumnWidth(3, 80)  # set size col width
        self.search_result.setColumnHidden(4, True)  # hide path column

    def load_tree(self, path=str(Path.home().as_posix())):
        default_dir = path
        self.tree_model = QFileSystemModel()
        self.tree_model.setFilter(QDir.Filter.AllDirs | QDir.Filter.NoDotAndDotDot)
        self.tree_model.setRootPath(default_dir)

        self.search_tree.setModel(self.tree_model)
        self.search_tree.setRootIndex(self.tree_model.index(default_dir))

        # Hide Size and Mod date columns
        self.search_tree.hideColumn(1)
        self.search_tree.hideColumn(2)
        self.search_tree.hideColumn(3)
        self.search_tree.setColumnWidth(0, 260)

        # set search bar to show root path
        self.search_box.setText(path)

    def load_click_functions(self):
        self.browse_button.clicked.connect(self.set_root_folder)
        self.search_tree.clicked.connect(self.get_file_in_tree_view)
        self.search_result.doubleClicked.connect(self.navigate_to_link)
        self.back_button.clicked.connect(self.directory_stack.visit_previous_page)
        self.next_button.clicked.connect(self.directory_stack.visit_next_page)
        self.up_button.clicked.connect(self.directory_stack.visit_parent_directory)

    def set_root_folder(self):
        default_dir = str(Path.home())
        path = QFileDialog.getExistingDirectory(self, "Select Root Folder", default_dir)
        if path:
            self.load_tree(path)
            self.search_box.setText(path)
            self.search_directory_content(path)

    # return tree view's selected file path
    def get_file_in_tree_view(self, index):
        index = self.tree_model.index(index.row(), 0, index.parent())
        filePath = self.tree_model.filePath(index)
        self.search_tree.setCurrentIndex(index)
        self.search_tree.scrollTo(index, QAbstractItemView.ScrollHint.PositionAtCenter)
        print("Selected File Path:", filePath)
        self.search_directory_content(filePath)

    def search_directory_content(self, path):
        try:
            # expand and focus file tree view to current item
            index = self.tree_model.index(path)
            self.search_tree.expand(index)
            self.search_tree.setCurrentIndex(index)
            self.search_tree.scrollTo(index, QAbstractItemView.ScrollHint.PositionAtCenter)

            # clear results from previous search
            self.file_table_model.removeRows(0, self.file_table_model.rowCount())

            # populate table
            path_obj = Path(path)
            for file in path_obj.iterdir():
                file_info = file.stat()
                name = file.name  # name
                size = str(utils.get_file_size_in_kb(file_info.st_size)) if file.is_file() else " "
                date = datetime.fromtimestamp(file_info.st_mtime).strftime('%d/%m/%Y %H:%M')
                type = Path(file.name).suffix if file.is_file() else "File Folder"
                path = str(file)
                item_list = [QStandardItem(name), QStandardItem(date), QStandardItem(type),
                             QStandardItem(size), QStandardItem(path)]
                self.file_table_model.appendRow(item_list)


        except WindowsError as e:
            print(e)
        except Exception as e:
            print(e)

    def navigate_to_link(self):
        row = self.search_result.selectionModel().currentIndex().row()
        item = self.file_table_model.item(row, 4)
        print(item.text())
        path = item.text()

        path_obj = Path(path)
        if path and path_obj.is_dir():
            self.search_directory_content(path)

    def open_item_in_os(self):
        indexes = self.search_result.selectedIndexes()
        item = self.file_table_model.itemFromIndex(indexes[-1])
        path = Path(item.text())
        if platform.system() == 'Darwin':  # macOS
            subprocess.call(('open', path))
        elif platform.system() == 'Windows':  # Windows
            os.startfile(path)
            # subprocess.call(['start', path], shell=True)
        else:  # linux variants
            subprocess.call(('xdg-open', path))


if __name__ == '__main__':
    try:
        app = QApplication([])
        window = MyApplication()
        app.exec()
    except Exception as e:
        print(e)
