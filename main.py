from pathlib import Path

from PyQt6.QtWidgets import *

from controller.create_folder_controller import CreateFolderController
from controller.main_view_controller import MainViewController
from view.create_folder_view import CreateFolderView

if __name__ == '__main__':
    try:
        app = QApplication([])
        folder_creation_controller = CreateFolderController(str(Path.home()))
        # controller = MainViewController()
        app.exec()
    except OSError as e:
        print(e)
    except Exception as e:
        print(e)


