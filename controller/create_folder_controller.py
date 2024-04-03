import os
import subprocess
from pathlib import Path
from sys import platform

from PyQt6.QtWidgets import QFileDialog, QMessageBox
from pathvalidate import sanitize_filepath

from view.create_folder_view import CreateFolderView
from view.error_message import ErrorMessageBox

# manages the create folder view and functionalities
# non-singleton: not aggregated by main view controller, instantiated only when called
class CreateFolderController:
    def __init__(self, main_view_controller, default_dir):
        self.main_view_controller = main_view_controller
        self.default_dir = default_dir
        self.create_folder_view = CreateFolderView(self, default_dir)

    # use QFileDialog to get location path (where user wants to make folders)
    def select_file_creation_path(self):
        try:
            selected_path = QFileDialog.getExistingDirectory(self.create_folder_view, "Select Folder to Create Files", self.default_dir)
            if not selected_path:
                return

            path = os.path.abspath(selected_path)
        except OSError as e:
            return ErrorMessageBox("OS Error", str(e))
        except Exception as e:
            return ErrorMessageBox("Error", str(e))
        else:
            self.create_folder_view.create_path_textbox.setText(path)

    # get folder names from text area, sanitize and return as list
    def parse_folder_names_text(self):
        try:
            cleaned_paths = []
            # extract line-by-line folder names
            text_input = self.create_folder_view.folder_names_textbox.toPlainText()
            if not text_input:
                return cleaned_paths
            separated_input = text_input.split("\n")
            for path in separated_input:
                if path.strip() == "":
                    continue
                # sanitize using pathvalidate lib
                cleaned_path = sanitize_filepath(path)
                cleaned_path = self.add_prefix_and_suffix(cleaned_path)
                cleaned_path = os.path.normpath(cleaned_path)
                cleaned_paths.append(cleaned_path) # add to list
            return cleaned_paths
        except OSError as e:
            raise OSError(e)
        except Exception as e:
            raise Exception(e)

    # add prefix / suffix to folder name (if user entered any)
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

    # function to create a directory
    def create_directory(self, path):
        try:
            my_path = Path(path)
            my_path.mkdir(parents=True, exist_ok=False)  # can add file exists handling
            return False, path
        except FileExistsError as e:
            return True, path
        except OSError as e:
            raise OSError(e) # pass to caller
        except Exception as e:
            raise Exception(e)

    # click the create folder button
    def create_folders(self):
        try:
            # get and sanitize path of folder creation
            raw_root_path = self.create_folder_view.create_path_textbox.text()
            root_path = os.path.abspath(sanitize_filepath(raw_root_path))

            # check exists and permissions
            if not os.path.exists(root_path):
                return ErrorMessageBox("File Path Error",
                                       f"Sorry, the selected creation path does not exist:\n{root_path}")
            if not os.access(root_path, os.W_OK):
                return ErrorMessageBox("Permission Error",
                                       f"You do not have access to write in the selected creation path:\n{root_path}")

            # get and process folder names input in text area
            folder_names_list = self.parse_folder_names_text()
            if len(folder_names_list) == 0:
                return ErrorMessageBox("Folder Creation Error",
                                       f"Please enter some folder names in the textbox.")

            no_files_created = True
            has_existing_files_flag = False
            existing_files_path_list = ""
            # process each file
            for folder_name in folder_names_list:
                # assemble new absolute path of folder to be created
                complete_path = os.path.abspath(root_path + os.sep + folder_name)
                # try create folder
                has_problems_creating_file, file_name = self.create_directory(complete_path)
                if has_problems_creating_file:
                    has_existing_files_flag = True
                    existing_files_path_list += file_name + "\n"
                    continue
                no_files_created = False # this will be True if any files created successfully

            if no_files_created and has_existing_files_flag:
                return ErrorMessageBox("File Exists Warning",
                                       f"Cannot create folder with existing names. See folder names below:",
                                       existing_files_path_list)

        except OSError as e:
            return ErrorMessageBox("OS Error", str(e))
        except Exception as e:
            return ErrorMessageBox("Error", str(e))
        else:
            # show success message box
            success_msg = QMessageBox()
            success_msg.setWindowTitle("Folders Created!")
            success_msg.setText("Folders created successfully.")
            success_msg.setIcon(QMessageBox.Icon.Information)
            if has_existing_files_flag:
                success_msg.setText("Folders created successfully.\nSome folders cannot be created "
                                    "because folders with same names exists: ")
                success_msg.setDetailedText(existing_files_path_list)
            success_msg.exec()
            # file browser visit folder creation page (if option is checked in window)
            if self.create_folder_view.explore_path_checkbox.isChecked():
                self.main_view_controller.visit_page_by_path_string(root_path)
                if root_path != self.main_view_controller.directory_stack.current_dir.path:
                    self.main_view_controller.directory_stack.visit_new_page(root_path)
                    self.main_view_controller.main_view.address_bar.setPlainText(root_path)
                self.main_view_controller.main_view.table_view.setFocus()

    # open file in local file manager (feature not fully implemented)
    def open_creation_directory_in_os(self, path):
        path = os.path.abspath(path)
        if platform.system() == 'Darwin':  # macOS
            subprocess.call(('open', path))
        elif platform.system() == 'Windows':  # Windows
            os.startfile(path)
            # subprocess.call(['start', path], shell=True)
        else:  # linux variants
            subprocess.call(('xdg-open', path))







