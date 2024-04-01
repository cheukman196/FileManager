import os
from PyQt6.QtWidgets import QFileDialog
from pathvalidate import sanitize_filepath

from view.create_folder_view import CreateFolderView
from view.error_message import ErrorMessageBox


class CreateFolderController:
    def __init__(self, default_dir):
        self.default_dir = default_dir
        self.create_folder_view = CreateFolderView(self, default_dir)

    def select_file_creation_path(self):
        try:
            selected_path = QFileDialog.getExistingDirectory(self.create_folder_view, "Select Folder to Create Files", self.default_dir)
            if not selected_path:
                return

            path = os.path.abspath(selected_path)
            if not os.path.exists(path):
                return ErrorMessageBox("File Path Error",
                                       f"Sorry, the selected path does not exist:\n{path}")
            if not os.access(path, os.W_OK):
                return ErrorMessageBox("Permission Error",
                                       f"You do not have access to write the given path:\n{path}")

        except OSError as e:
            return ErrorMessageBox("OS Error", str(e))
        except Exception as e:
            return ErrorMessageBox("Error", str(e))
        else:
            self.create_folder_view.create_path_textbox.setText(path)

    def parse_folder_names_text(self):
        try:
            text_input = self.create_folder_view.folder_names_textbox.toPlainText()
            if not text_input:
                print("no text")
                return
            separated_input = text_input.split("\n")
            print(separated_input)
            cleaned_paths = []
            for path in separated_input:
                if path.strip() == "":
                    continue
                cleaned_path = sanitize_filepath(path)
                cleaned_path = self.add_prefix_and_suffix(cleaned_path)
                cleaned_path = os.path.normpath(cleaned_path)

                cleaned_paths.append(cleaned_path)
                print(cleaned_path)
            return cleaned_paths
        except OSError as e:
            print(e.args)
        except Exception as e:
            print(e.args)

    def add_prefix_and_suffix(self, path):
        if self.create_folder_view.add_prefix_checkbox.isChecked():
            prefix = self.create_folder_view.add_prefix_textbox.text()
            if prefix and prefix.strip() != "":
                cleaned_prefix = sanitize_filepath(prefix)
                path = str(cleaned_prefix) + str(path)
        if self.create_folder_view.add_suffix_checkbox.isChecked():
            suffix = self.create_folder_view.add_suffix_textbox.text()
            if suffix and suffix.strip() != "":
                cleaned_suffix = sanitize_filepath(suffix)
                path = str(path) + str(cleaned_suffix)
        return path





