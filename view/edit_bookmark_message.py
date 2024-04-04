from pathlib import Path
from pydoc import html

from PyQt6 import uic
from PyQt6.QtWidgets import *

from view.error_message import ErrorMessageBox


class EditBookmarkMessage(QDialog):
    def __init__(self, name, link, bookmarks_controller):
        super().__init__()
        uic.loadUi("ui/edit_bookmark.ui", self) # load .ui file
        self.show()
        self.setFocus()

        self.bookmarks_controller = bookmarks_controller

        # get visual elements
        self.name_textbox = self.findChild(QLineEdit, "name_textbox")
        self.link_textbox = self.findChild(QLineEdit, "link_textbox")
        self.button_box = self.findChild(QDialogButtonBox, "button_box")

        # set visual elements
        self.name_textbox.setText(name)
        self.link_textbox.setText(link)

        # set button functions
        self.init_click_functions()


    def init_click_functions(self):
        self.button_box.button(QDialogButtonBox.StandardButton.Save).clicked.connect(self.parse_text_input)
        self.button_box.button(QDialogButtonBox.StandardButton.Cancel).clicked.connect(self.close)

    def parse_text_input(self):
        name_input = html.escape(self.name_textbox.text())
        link_input = html.escape(self.link_textbox.text())

        # check inputs
        if not name_input or name_input == "":
            return ErrorMessageBox("Input Error", "Please provide a name for the bookmark.")

        if not link_input or link_input == "":
            return ErrorMessageBox("Input Error", "Please provide a link for the bookmark.")
        elif not Path(link_input).exists():
            return ErrorMessageBox("Path Error", "The link for the bookmark points to a folder that doesn't exist.")
        elif not Path(link_input).is_dir():
            return ErrorMessageBox("Path Error", "The link for the bookmark must point to a folder.")

        self.close()
        self.bookmarks_controller.edit_bookmark(name_input, link_input)
        return





