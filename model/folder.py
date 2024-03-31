import os
from pathlib import Path

import utils


class Folder:
    def __init__(self, path):
        self.path = os.path.abspath(path)
        self.name = utils.get_current_directory_name(path)
        self.parent = utils.get_parent_directory_name(self.path) if os.sep in utils.get_parent_directory_name(self.path) \
            else os.path.abspath(os.sep)
        self.next = None

    def print_details(self):
        print(f"Path: {self.path}")
        print(f"Name: {self.name}")
        print(f"Parent: {self.parent}")
        print(f"Next: {self.next}")
        print()

