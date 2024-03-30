import os

import utils


class Folder:
    def __init__(self, path):
        self.path = path
        self.name = utils.get_current_directory_name(path)
        self.parent = utils.get_parent_directroy_name(path)
        self.next = None

    def print_details(self):
        print(f"Path: {self.path}")
        print(f"Name: {self.name}")
        print(f"Parent: {self.parent}")
        print(f"Next: {self.next}")
        print()


# f1 = Folder(r"C:")
# f2 = Folder(r"C:\Users\CM\Documents\_Documents\GBC\Year 2_Sem 2")
# f1.print_details()
# f2.print_details()

