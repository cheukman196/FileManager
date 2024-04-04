import os
from pathlib import Path

from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import *

from controller.create_folder_controller import CreateFolderController
from controller.main_view_controller import MainViewController
from view.create_folder_view import CreateFolderView

if __name__ == '__main__':
    app = QApplication([])
    controller = MainViewController()

    window_logo_icon = QIcon("icon\\logo.png")
    app.setWindowIcon(window_logo_icon)
    app.exec()


