from pathlib import Path

from model.folder import Folder
from model.stack import Stack


class DirectoryStack:
    def __init__(self, root_dir_path):
        self.back_stack = Stack()
        self.next_stack = Stack()
        self.root_dir = Folder(root_dir_path)
        self.current_dir = Folder(root_dir_path)
        self.can_visit_prev = False
        self.can_visit_next = False
        self.can_visit_parent = False

    def visit_new_page(self, new_page_path):
        self.back_stack.push(self.current_dir)
        self.next_stack.clear()
        self.current_dir = Folder(new_page_path)
        self.update_directory_stack_status()

    def visit_previous_page(self):
        self.next_stack.push(self.current_dir)
        self.current_dir = self.back_stack.pop()
        self.update_directory_stack_status()

    def visit_next_page(self):
        self.back_stack.push(self.current_dir)
        self.current_dir = self.next_stack.pop()
        self.update_directory_stack_status()

    def visit_parent_directory(self):
        if self.current_dir != self.root_dir:
            self.back_stack.push(self.current_dir)
            self.next_stack.clear()
            self.current_dir = Folder(self.current_dir.parent)
            self.update_directory_stack_status()

    def update_directory_stack_status(self):
        # update status flags based on stacks and if we are at root directory
        self.can_visit_prev = self.back_stack.size() == 0
        self.can_visit_next = self.next_stack.size() == 0
        self.can_visit_parent = self.current_dir != self.root_dir


