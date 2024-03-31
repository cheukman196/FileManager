import os
from pathlib import Path

from PyQt6.QtCore import QDir
from PyQt6.QtGui import QFileSystemModel

from view.error_message import ErrorMessageBox


# manages QTreeView in main view
# has reference to a QFileSystemModel that handles system file structure
# has reference to the main_view
class DirectoryTreeController:
    INITIAL_PATH = os.path.expanduser('~')

    def __init__(self, main_view):
        self.tree_model = QFileSystemModel()
        self.main_view = main_view
        self.load_tree()

    def load_tree(self, path=os.path.expanduser('~')):
        try:
            # update model
            self.tree_model = QFileSystemModel()
            self.tree_model.setFilter(QDir.Filter.AllDirs | QDir.Filter.NoDotAndDotDot)
            self.tree_model.setRootPath(path)
            # update view's model reference and set root index for view
            self.main_view.update_tree_view(self.tree_model, path)
        except PermissionError as e:
            ErrorMessageBox("Permission Error", str(e))
            print(e)
        except Exception as e:
            ErrorMessageBox("Error", str(e))
            print(e)
        else:
            # update root path text box
            self.main_view.search_box.setText(path)

    def get_index_by_path(self, path):
        return self.tree_model.index(path)
