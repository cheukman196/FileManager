from typing import override

from PyQt6 import uic
from PyQt6.QtWidgets import *

# Window that creates folders (see ui/create_folder.ui)
class BookmarksView(QWidget):
    def __init__(self, bookmarks_controller, current_path):
        super().__init__()
        uic.loadUi("ui/bookmarks.ui", self) # load .ui file
        self.show()

        self.bookmarks_controller = bookmarks_controller

        # get visual elements
        self.current_page_textbox = self.findChild(QLineEdit, "current_page_textbox")
        self.bookmark_name_textbox = self.findChild(QLineEdit, "bookmark_name_textbox")
        self.my_bookmarks_list = self.findChild(QListWidget, "my_bookmarks_list")
        self.add_bookmark_button = self.findChild(QPushButton, "add_bookmark_button")
        self.visit_bookmark_button = self.findChild(QPushButton, 'visit_bookmark_button')
        self.delete_bookmark_button = self.findChild(QPushButton, 'delete_bookmark_button')
        self.edit_bookmark_button = self.findChild(QPushButton, 'edit_bookmark_button')
        self.return_button = self.findChild(QPushButton, 'return_button')

        # set visual elements
        self.current_page_textbox.setText(current_path)
        self.bookmark_name_textbox.setFocus()

        # set button functions
        self.init_click_functions()


    def init_click_functions(self):
        self.return_button.clicked.connect(self.close)
        self.add_bookmark_button.clicked.connect(self.bookmarks_controller.add_bookmark)
        self.my_bookmarks_list.itemClicked.connect(self.bookmarks_controller.click_bookmark)
        self.my_bookmarks_list.itemDoubleClicked.connect(self.bookmarks_controller.double_click_bookmark)
        self.visit_bookmark_button.clicked.connect(self.bookmarks_controller.visit_bookmark)
        self.edit_bookmark_button.clicked.connect(self.bookmarks_controller.open_edit_bookmark_message)
        self.delete_bookmark_button.clicked.connect(self.bookmarks_controller.delete_bookmark)

    def enable_bookmark_buttons(self, bool_value):
        self.visit_bookmark_button.setEnabled(bool_value)
        self.edit_bookmark_button.setEnabled(bool_value)
        self.delete_bookmark_button.setEnabled(bool_value)

