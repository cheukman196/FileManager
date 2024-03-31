import os
from pathlib import Path

from PyQt6 import uic
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QStandardItemModel, QFileSystemModel, QIcon
from PyQt6.QtWidgets import *

# main view for application (type: QMainWindow)
class MainView(QMainWindow):
    def __init__(self, main_view_controller):
        super(MainView, self).__init__()
        uic.loadUi("ui/main.ui", self) # load .ui file
        self.show()

        # reference to main controller
        self.main_view_controller = main_view_controller

        # initialize model references (models will be updated and injected by controllers
        self.table_model = QStandardItemModel(0, 5)
        self.table_model.setHorizontalHeaderLabels(['Name', 'Date Modified', 'Type', 'Size', 'Path'])
        self.tree_model = QFileSystemModel()

        # get all visual elements in .ui file
        self.browse_button = self.findChild(QPushButton, "browse_file_button")
        self.search_box = self.findChild(QLineEdit, "search_box")
        self.address_bar = self.findChild(QLineEdit, "address_bar")
        self.table_view = self.findChild(QTableView, "search_result")
        self.tree_view = self.findChild(QTreeView, "search_tree")
        self.back_button = self.findChild(QPushButton, "back_button")
        self.up_button = self.findChild(QPushButton, "up_button")
        self.next_button = self.findChild(QPushButton, "next_button")
        self.refresh_button = self.findChild(QPushButton, "refresh_button")

        # config view settings
        self.table_view.setColumnHidden(4, True)  # hide path column
        self.table_view.setColumnWidth(0, 300)  # set name col width
        self.table_view.setColumnWidth(2, 80)  # set type col width
        self.table_view.setColumnWidth(3, 80)  # set size col width

        self.init_tree_view()
        self.init_click_functions()
        self.init_button_icons()

    def init_tree_view(self, path=os.path.expanduser('~')):
        self.tree_view.setModel(self.tree_model)
        self.tree_view.setRootIndex(self.tree_model.index(path))

        # Hide Size and Mod date columns
        self.tree_view.hideColumn(1)
        self.tree_view.hideColumn(2)
        self.tree_view.hideColumn(3)
        self.tree_view.setColumnWidth(0, 260)

        # set search bar to show root path
        self.search_box.setText(path)
        self.address_bar.setText(path)

    def init_table_view(self):
        self.table_view.setColumnHidden(4, True)  # hide path column
        self.table_view.setColumnWidth(0, 300)  # set name col width
        self.table_view.setColumnWidth(1, 120)  # set name col width
        self.table_view.setColumnWidth(2, 80)  # set type col width
        self.table_view.setColumnWidth(3, 80)  # set size col width


    def init_button_icons(self):
        back_icon = QIcon("icon\\left.png")
        self.back_button.setIcon(back_icon)
        self.back_button.setIconSize(QSize(10, 10))

        up_icon = QIcon("icon\\up.png")
        self.up_button.setIcon(up_icon)
        self.up_button.setIconSize(QSize(14, 14))

        next_icon = QIcon("icon\\right.png")
        self.next_button.setIcon(next_icon)
        self.next_button.setIconSize(QSize(12, 12))

        refresh_icon = QIcon("icon\\refresh.png")
        self.refresh_button.setIcon(refresh_icon)
        self.refresh_button.setIconSize(QSize(12, 12))

    def init_click_functions(self):
        assert isinstance(self.main_view_controller.reset_root_folder, object)

        self.browse_button.clicked.connect(self.main_view_controller.reset_root_folder)
        self.tree_view.clicked.connect(self.main_view_controller.get_file_in_tree_view)
        self.table_view.doubleClicked.connect(self.main_view_controller.get_file_in_table_view)
        self.back_button.clicked.connect(self.main_view_controller.click_back_button)
        self.next_button.clicked.connect(self.main_view_controller.click_next_button)
        self.up_button.clicked.connect(self.main_view_controller.click_up_button)
        self.refresh_button.clicked.connect(self.main_view_controller.visit_page_by_path_string)

        self.browse_button.clicked.connect(self.main_view_controller.update_navigation_bar_and_button_state)
        self.tree_view.clicked.connect(self.main_view_controller.update_navigation_bar_and_button_state)
        self.table_view.doubleClicked.connect(self.main_view_controller.update_navigation_bar_and_button_state)
        self.back_button.clicked.connect(self.main_view_controller.update_navigation_bar_and_button_state)
        self.next_button.clicked.connect(self.main_view_controller.update_navigation_bar_and_button_state)
        self.up_button.clicked.connect(self.main_view_controller.update_navigation_bar_and_button_state)

    #
    def tree_view_scroll_to_index(self, index):
        self.tree_view.expand(index)
        self.tree_view.setCurrentIndex(index)
        self.tree_view.scrollTo(index, QAbstractItemView.ScrollHint.PositionAtCenter)

    def update_tree_view(self, tree_model, path=os.path.expanduser('~')):
        self.tree_model = tree_model
        self.tree_view.setModel(self.tree_model)
        self.tree_view.setRootIndex(self.tree_model.index(path))

