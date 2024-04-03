import os
from pathlib import Path

from model.folder import Folder
from model.stack import Stack


# handles file explorer back, next and parent directory buttons
# uses dual stacks to track previous page, next page and current directory
class DirectoryStack:
    def __init__(self, root_dir_path):
        self.back_stack = Stack()
        self.next_stack = Stack()
        self.root_dir = Folder(root_dir_path)
        self.current_dir = Folder(root_dir_path)
        self.can_visit_prev = False
        self.can_visit_next = False
        self.can_visit_parent = False

    # visit any new page (NOT by the arrow buttons)
    # reset_root_folder resets the stack
    def visit_new_page(self, new_page_path):
        self.back_stack.push(self.current_dir)
        self.next_stack.clear()
        self.current_dir = Folder(new_page_path)
        self.update_directory_stack_status()

    # press back button
    def visit_previous_page(self):
        self.next_stack.push(self.current_dir)
        self.current_dir = self.back_stack.pop()
        self.update_directory_stack_status()

    # press next button
    def visit_next_page(self):
        self.back_stack.push(self.current_dir)
        self.current_dir = self.next_stack.pop()
        self.update_directory_stack_status()

    # press up button
    def visit_parent_directory(self):
        if self.current_dir != self.root_dir:
            self.back_stack.push(self.current_dir)
            self.next_stack.clear()
            self.current_dir = Folder(self.current_dir.parent)
            self.update_directory_stack_status()

    # update directory stack status (statuses used to disable / enable buttons)
    def update_directory_stack_status(self):
        # update status flags based on stacks and if we are at root directory
        self.can_visit_prev = not self.back_stack.empty()
        self.can_visit_next = not self.next_stack.empty()
        self.can_visit_parent = self.current_dir.path != os.path.abspath(os.sep) # if not system root

    # on main controller resetting root directory, reset directory stack as well
    def reset_root_directory(self, new_root_dir_path):
        self.back_stack.clear()
        self.next_stack.clear()
        self.root_dir = Folder(new_root_dir_path)
        self.current_dir = Folder(new_root_dir_path)
        self.update_directory_stack_status()
