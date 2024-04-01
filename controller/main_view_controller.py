import os
import subprocess
from pathlib import Path
from sys import platform

from PyQt6.QtWidgets import QFileDialog
from controller.directory_table_controller import DirectoryTableController
from controller.directory_tree_controller import DirectoryTreeController
from model.directory_stack import DirectoryStack
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

    def get_file_in_table_view(self):
        try:
            table_view = self.main_view.table_view
            table_model = self.table_controller.table_model

            # get selected row to return path
            row = table_view.selectionModel().currentIndex().row()
            item = table_model.item(row, 4)
            path = item.text()
            self.visit_page_by_path_string(path)
        except PermissionError as e:
            print("Permission Exception")
            return ErrorMessageBox("Permission Error", str(e))
        except OSError as e:
            print("OS Exception")
            ErrorMessageBox("OS Error", str(e))

        except Exception as e:
            print("General Exception")
            ErrorMessageBox("Error", str(e))
            # raise Exception(e)
        else:
            print("Else Block")
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
            print(self.directory_stack.current_dir.parent)
            parent_directory = self.directory_stack.current_dir.parent
            path = parent_directory
            print(path)
            if not path:
                ErrorMessageBox("Directory Stack Error", "No parent page found.")
                return
            self.visit_page_by_path_string(path)
            self.directory_stack.visit_new_page(path)
        except OSError as e:
            ErrorMessageBox("OS Error", str(e))
            return
        except Exception as e:
            ErrorMessageBox("Error", str(e))
            return

    def reset_root_folder(self):
        try:
            default_dir = os.path.expanduser('~')
            print(default_dir)
            selected_path = QFileDialog.getExistingDirectory(self.main_view, "Select Root Folder", default_dir)

            if selected_path:
                path = os.path.abspath(selected_path)
                self.tree_controller.load_tree(path)
                self.table_controller.search_directory_contents(path)
                # update root directory text box
                self.main_view.search_box.setText(path)
                self.directory_stack.reset_root_directory(path)
        except OSError as e:
            ErrorMessageBox("OS Error", str(e))
            return
        except Exception as e:
            ErrorMessageBox("Error", str(e))
            return

    def update_navigation_bar_and_button_state(self):
        self.main_view.back_button.setEnabled(self.directory_stack.can_visit_prev)
        self.main_view.next_button.setEnabled(self.directory_stack.can_visit_next)
        self.main_view.up_button.setEnabled(self.directory_stack.can_visit_parent)
        self.main_view.address_bar.setText(self.directory_stack.current_dir.path)

    def open_table_view_directory_in_os(self):
        indexes = self.main_view.table_view.selectedIndexes()
        item = self.table_controller.table_model.itemFromIndex(indexes[-1])
        path = Path(item.text())
        if platform.system() == 'Darwin':  # macOS
            subprocess.call(('open', path))
        elif platform.system() == 'Windows':  # Windows
            os.startfile(path)
            # subprocess.call(['start', path], shell=True)
        else:  # linux variants
            subprocess.call(('xdg-open', path))
