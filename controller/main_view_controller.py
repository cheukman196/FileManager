import os
import subprocess
from pathlib import Path
from sys import platform

from PyQt6.QtWidgets import *
from PyQt6.QtWidgets import QFileDialog
from controller.directory_table_controller import DirectoryTableController
from controller.directory_tree_controller import DirectoryTreeController
from model.directory_stack import DirectoryStack
from view.main_view import MainView


class MainViewController:
    def __init__(self):
        self.directory_stack = DirectoryStack(str(Path.home()))

        self.main_view = MainView(self)

        self.table_controller = DirectoryTableController(self.main_view)
        self.tree_controller = DirectoryTreeController(self.main_view)

    def reset_root_folder(self):
        try:
            default_dir = str(Path.home())
            print(default_dir)
            path = QFileDialog.getExistingDirectory(self.main_view, "Select Root Folder", default_dir)
            # dialog = QFileDialog(self.main_view, "Select Root Folder", default_dir)
            # dialog.setOption(QFileDialog.Option.ShowDirsOnly, True)
            # path = QFileDialog.getExistingDirectory()
            print("Result dir: " + path)
            if path:
                # update tree view and scroll to item
                self.tree_controller.load_tree(path)
                self.table_controller.search_directory_contents(path)
                # update root directory text box
                self.main_view.search_box.setText(path)
        except WindowsError as e:
            print(e)
        except Exception as e:
            print(e)

    def get_file_in_tree_view(self):
        index_obj = self.main_view.tree_view.currentIndex() # returns QStandardModelIndex
        print(str(index_obj.row()) + " " + str(index_obj.column()))
        index_literal = self.tree_controller.tree_model.index(index_obj.row(), 0, index_obj.parent())
        print(str(index_literal.row()) + " " + str(index_literal.column()))
        file_path = self.tree_controller.tree_model.filePath(index_obj)
        print("Selected File Path:", file_path)

        self.table_controller.search_directory_contents(file_path) # update table view
        print("hi")
        # !! COULD TWEAK TO NOT CENTER !!
        self.main_view.tree_view_scroll_to_index(index_literal) # update tree view
        print("hi")

    def get_file_in_table_view(self):
        table_view = self.main_view.table_view
        table_model = self.table_controller.table_model

        # get selected row
        row = table_view.selectionModel().currentIndex().row()
        item = table_model.item(row, 4)

        print(item.text())
        path = item.text()
        path_obj = Path(path)
        if path and path_obj.is_dir():
            self.table_controller.search_directory_contents(path)
            index = self.tree_controller.get_index_by_path(path)
            self.main_view.tree_view_scroll_to_index(index)

    def open_table_view_directory_in_os(self):
        indexes = self.main_view.table_view.selectedIndexes()
        item = self.table_controller.table_model.itemFromIndex(indexes[-1])
        path = Path(item.text())
        if platform.system() == 'Darwin':  # macOS
            subprocess.call(('open', path))
        elif platform.system() == 'Windows':  # Windows
            os.startfile(path)
            # subprocess.call(['start', path], shell=True)
        else:  # linux variants
            subprocess.call(('xdg-open', path))