import os
from pathlib import Path

from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import QFileDialog

from controller.create_folder_controller import CreateFolderController
from controller.directory_table_controller import DirectoryTableController
from controller.directory_tree_controller import DirectoryTreeController
from model.directory_stack import DirectoryStack
from service.utils import relocate_file, copy_file
from view.error_message import ErrorMessageBox
from view.main_view import MainView


# main controller for main view
# has two sub-controllers for two widgets (directory_tree_controller, directory_table_controller)
# has access to main-view .ui page (main_view)
# has a directory stack to manage previous/next/parent page functions
class MainViewController:
    def __init__(self):
        self.directory_stack = DirectoryStack(os.path.expanduser('~'))

        self.main_view = MainView(self)

        self.table_controller = DirectoryTableController(self.main_view)
        self.tree_controller = DirectoryTreeController(self.main_view)

    # takes path string, updates tree view and table view accordingly
    def visit_page_by_path_string(self, path=""):
        try:
            path = path if path else self.directory_stack.current_dir.path
            path_obj = Path(path)
            # only load of path exists and is a directory
            if path and path_obj.is_dir():
                self.table_controller.search_directory_contents(path)  # load table view
                index = self.tree_controller.get_index_by_path(path)
                self.main_view.tree_view_scroll_to_index(index)  # load tree view
        except OSError as e:
            raise OSError("visit page by string raised error")
        except Exception as e:
            raise Exception("visit page by string raised error")

    # click on directory tree, navigate to file
    def get_file_in_tree_view(self):
        try:
            index_obj = self.main_view.tree_view.currentIndex()
            path = self.tree_controller.tree_model.filePath(index_obj)
            self.visit_page_by_path_string(path)
        except PermissionError as e:
            return ErrorMessageBox("Permission Error", str(e))
        except OSError as e:
            return ErrorMessageBox("OS Error", str(e))
        except Exception as e:
            return ErrorMessageBox("Error", str(e))
        else:
            self.directory_stack.visit_new_page(path)

    # click on directory table, navigate to file
    def get_file_in_table_view(self):
        try:
            table_view = self.main_view.table_view
            table_model = self.table_controller.table_model

            # get selected row to return path
            row = table_view.selectionModel().currentIndex().row()
            item = table_model.item(row, 4)
            path = item.text()
            if not Path(path).is_dir():
                return
            self.visit_page_by_path_string(path)
        except PermissionError as e:
            return ErrorMessageBox("Permission Error", str(e))
        except OSError as e:
            ErrorMessageBox("OS Error", str(e))
        except Exception as e:
            ErrorMessageBox("Error", str(e))
        else:
            self.directory_stack.visit_new_page(path)


    def click_back_button(self):
        try:
            prev_folder_item = self.directory_stack.back_stack.peek()
            if not prev_folder_item:
                return ErrorMessageBox("Directory Stack Error", "No previous page was cached.")

            path = prev_folder_item.path
            self.visit_page_by_path_string(path)
        except OSError as e:
            return ErrorMessageBox("OS Error", str(e))
        except Exception as e:
            return ErrorMessageBox("Error", str(e))
        else:
            self.directory_stack.visit_previous_page()

    def click_next_button(self):
        try:
            next_folder_item = self.directory_stack.next_stack.peek()
            if not next_folder_item:
                return ErrorMessageBox("Directory Stack Error", "No next page was cached.")
            path = next_folder_item.path
            self.visit_page_by_path_string(path)
        except OSError as e:
            return ErrorMessageBox("OS Error", str(e))
        except Exception as e:
            return ErrorMessageBox("Error", str(e))
        else:
            self.directory_stack.visit_next_page()

    def click_up_button(self):
        try:
            parent_directory = self.directory_stack.current_dir.parent
            path = parent_directory
            if not path:
                ErrorMessageBox("Directory Stack Error", "No parent page found.")
                return
            self.visit_page_by_path_string(path)
        except OSError as e:
            ErrorMessageBox("OS Error", str(e))
            return
        except Exception as e:
            ErrorMessageBox("Error", str(e))
        else:
            self.directory_stack.visit_new_page(path)


    def reset_root_folder(self):
        try:
            default_dir = os.path.expanduser('~')
            selected_path = QFileDialog.getExistingDirectory(self.main_view, "Select Root Folder", default_dir)

            if selected_path:
                path = os.path.abspath(selected_path)
                self.tree_controller.load_tree(path)
                self.table_controller.search_directory_contents(path)
                # update root directory text box
                self.main_view.search_box.setText(path)
                self.directory_stack.reset_root_directory(path)
        except OSError as e:
            return ErrorMessageBox("OS Error", str(e))

        except Exception as e:
            return ErrorMessageBox("Error", str(e))

    def open_create_folders_window(self):
        CreateFolderController(self, self.directory_stack.current_dir.path)

    def update_navigation_bar_and_button_state(self):
        self.main_view.back_button.setEnabled(self.directory_stack.can_visit_prev)
        self.main_view.next_button.setEnabled(self.directory_stack.can_visit_next)
        self.main_view.up_button.setEnabled(self.directory_stack.can_visit_parent)
        self.main_view.address_bar.setText(self.directory_stack.current_dir.path)

    def click_move_files_button(self):
        try:
            destination_path = self.directory_stack.current_dir.path
            selected_path = QFileDialog.getOpenFileUrls(self.main_view, 'Select Files to move to folder', QUrl(destination_path))[0]
            if len(selected_path) > 0:
                for path in selected_path:
                    path = os.path.normpath(path.path()).lstrip(os.sep)
                    relocate_file(path, destination_path)
                self.main_view.refresh_button.click()
        except OSError as e:
            return ErrorMessageBox("OS Error",
                                       "Source file or destination folder is missing.", str(e))
        except Exception as e:
            return ErrorMessageBox("Unexpected Error", str(e))


    def click_copy_files_button(self):
        try:
            destination_path = self.directory_stack.current_dir.path
            selected_path = QFileDialog.getOpenFileUrls(self.main_view, "Select Files to copy to folder", QUrl(destination_path))[0]
            if len(selected_path) > 0:
                for path in selected_path:
                    path = os.path.normpath(path.path()).lstrip(os.sep)
                    copy_file(path, destination_path)
                self.main_view.refresh_button.click()
        except OSError as e:
            return ErrorMessageBox("OS Error",
                                   "Source file or destination folder is missing.", str(e))
        except Exception as e:
            return ErrorMessageBox("Unexpected Error", str(e))

