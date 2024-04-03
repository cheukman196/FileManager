from PyQt6 import uic
from PyQt6.QtWidgets import *

# Window that creates folders (see ui/create_folder.ui)
class CreateFolderView(QWidget):
    def __init__(self, create_folder_controller, file_creation_path=""):
        super().__init__()
        uic.loadUi("ui/create_folder.ui", self) # load .ui file
        self.show()

        self.create_folder_controller = create_folder_controller

        # get visual elements
        self.create_path_label = self.findChild(QLabel, "create_path_label")
        self.create_path_textbox = self.findChild(QLineEdit, "create_path_textbox")
        self.create_path_button = self.findChild(QPushButton, "create_path_button")
        self.add_prefix_checkbox = self.findChild(QCheckBox, "add_prefix_checkbox")
        self.add_prefix_textbox = self.findChild(QLineEdit, "add_prefix_textbox")
        self.add_suffix_checkbox = self.findChild(QCheckBox, "add_suffix_checkbox")
        self.add_suffix_textbox = self.findChild(QLineEdit, "add_suffix_textbox")
        self.explore_path_checkbox = self.findChild(QCheckBox, "explore_path_checkbox")
        self.textarea_label = self.findChild(QLabel, "textarea_label")
        self.folder_names_textbox = self.findChild(QTextEdit, "folder_names_textbox")
        self.tip_textbrowser = self.findChild(QTextBrowser, "tip_textbrowser")
        self.create_folders_button = self.findChild(QPushButton, "create_folders_button")
        self.return_button = self.findChild(QPushButton, "return_button")

        # set visual elements
        self.create_path_textbox.setText(file_creation_path)
        self.folder_names_textbox.setFocus()

        # set button functions
        self.init_click_functions()


    def init_click_functions(self):
        self.add_prefix_checkbox.clicked.connect(self.toggle_prefix_textbox)
        self.add_suffix_checkbox.clicked.connect(self.toggle_suffix_textbox)
        self.return_button.clicked.connect(self.close)
        self.create_path_button.clicked.connect(self.create_folder_controller.select_file_creation_path)
        self.create_folders_button.clicked.connect(self.create_folder_controller.create_folders)

    def toggle_prefix_textbox(self):
        self.add_prefix_textbox.setEnabled(self.add_prefix_checkbox.isChecked())
        self.add_prefix_textbox.setFocus()

    def toggle_suffix_textbox(self):
        self.add_suffix_textbox.setEnabled(self.add_suffix_checkbox.isChecked())
        self.add_suffix_textbox.setFocus()