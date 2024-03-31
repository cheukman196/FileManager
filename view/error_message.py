import string
from cmath import e

from PyQt6.QtWidgets import QMessageBox

# Error Message popup (will pop-up on initializing)
class ErrorMessageBox:
    def __init__(self, title, message, details=""):
        self.error_message_box = QMessageBox()
        self.error_message_box.setWindowTitle(title)
        self.error_message_box.setText("Oops, seems like we have a problem: ")
        self.error_message_box.setInformativeText(message)
        self.error_message_box.setDetailedText(details)
        self.error_message_box.setIcon(QMessageBox.Icon.Warning)
        self.error_message_box.exec()