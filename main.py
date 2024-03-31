from PyQt6.QtWidgets import *
from controller.main_view_controller import MainViewController

if __name__ == '__main__':
    try:
        app = QApplication([])
        # window = MyApplication()
        controller = MainViewController()
        app.exec()
    except OSError as e:
        print(e)
    except Exception as e:
        print(e)


