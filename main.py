from pathlib import Path
# from PySide6.QtWidgets import QFileSystemModel
from PyQt6 import uic
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
# from PySide6.QtCore import *


class MyApplication(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI/main.ui", self)
        self.show()

        self.search_button = self.findChild(QPushButton, "search_button")
        self.search_box = self.findChild(QLineEdit, "search_box")
        self.search_box_warning = self.findChild(QLabel, "search_box_warning")
        self.search_result = self.findChild(QListWidget, "search_result")
        self.search_tree = self.findChild(QTreeView, "search_tree")
        self.browse_button = self.findChild(QPushButton, "browse_file_button")
        self.load_tree()

        self.search_button.clicked.connect(self.search)
        self.browse_button.clicked.connect(self.find_file_path)

    # C:\Users\CM\Documents\Tools3
    def search(self):
        try:
            self.search_result.clear()   # clear previous records
            path = self.search_box.text()
            path_obj = Path(path)
            if path == "":
                self.search_box_warning.setText("No directories selected. Enter a path or select a file.")
                return
            if not path_obj.is_dir():
                self.search_box_warning.setText("Not a valid directory / folder. Please select a folder instead.")
                return

            # populate list
            files = path_obj.iterdir()
            for file in files:
                if file.is_dir() or file.is_file():
                    item = QListWidgetItem(file.name)
                    self.search_result.addItem(item)
            # create model and populate tree
            self.search_box_warning.setText("Search complete.")

        except WindowsError as e:
            print(e)
        except Exception as e:
            print(e)

        # use file dialog to return tuple into path
    def find_file_path(self):
        default_dir = str(Path.home()) + "\\Documents"
        print(default_dir)
        # path = QFileDialog.getOpenFileName(self, "Open File", str(Path.home()), "All Files (*);;Images (*.png *.gif *svg *.jpg);;PDFs (*.pdf);;Word files (*.doc, *.docx, *.rtf);;Excel files (*.xls, *.xlsx);;PowerPoint files (*.ppt, *.pptx);;Text files (*.txt)")
        path = QFileDialog.getExistingDirectory(self, "Open File", default_dir)
        if path:
            self.search_box.setText(path)
            self.search()

    def load_tree(self):
        default_dir = str(Path.home())
        self.model = QFileSystemModel()
        self.model.setFilter(QDir.Filter.AllDirs | QDir.Filter.NoDotAndDotDot)
        self.model.setRootPath(default_dir)

        self.search_tree.setModel(self.model)
        self.search_tree.setRootIndex(self.model.index(default_dir))

        # Hide Size and Mod date columns
        self.search_tree.hideColumn(2)
        self.search_tree.hideColumn(3)
        self.search_tree.setColumnWidth(0, 500)





if __name__ == '__main__':
    app = QApplication([])
    window = MyApplication()
    app.exec()
