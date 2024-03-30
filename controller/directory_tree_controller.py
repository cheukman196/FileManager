from pathlib import Path

from PyQt6.QtCore import QDir, QModelIndex
from PyQt6.QtGui import QFileSystemModel
from PyQt6.QtWidgets import QFileDialog


class DirectoryTreeController:
    INITIAL_PATH = str(Path.home())
    def __init__(self, main_view):
        self.tree_model = QFileSystemModel()
        self.main_view = main_view
        self.load_tree()

    def load_tree(self, path=str(Path.home().as_posix())):
        try:
            # update model
            self.tree_model = QFileSystemModel()
            self.tree_model.setFilter(QDir.Filter.AllDirs | QDir.Filter.NoDotAndDotDot)
            self.tree_model.setRootPath(path)
            print("Root: " + path)
            # update view's model reference and set root index for view
            # view_model = self.main_view.tree_model
            # self.main_view.tree_model = self.tree_model
            self.main_view.update_tree_view(self.tree_model, path)
        except PermissionError as e:
            print(e)
        except Exception as e:
            print(e)

        # update root path text box
        self.main_view.search_box.setText(path)

    def get_index_by_path(self, path):
        return self.tree_model.index(path)




