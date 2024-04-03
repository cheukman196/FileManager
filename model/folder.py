import os

from service import utils

# Folder class handles folder objects, used in DirectoryStack and path tracking
class Folder:
    def __init__(self, path):
        self.path = os.path.abspath(path) # path of directory
        self.name = utils.get_current_directory_name(path) # e.g. file.txt
        self.parent = utils.get_parent_directory_name(self.path) if os.sep in utils.get_parent_directory_name(self.path) \
            else os.path.abspath(os.sep) # parent folder e.g. C:/User/Dave/aa.txt has a parent of C:/User/Dave
        self.next = None # reference for stack

    def print_details(self):
        print(f"Path: {self.path}")
        print(f"Name: {self.name}")
        print(f"Parent: {self.parent}")
        print(f"Next: {self.next}")
        print()

