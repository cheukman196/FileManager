import os
import shutil
import sqlite3
from pathlib import Path
from datetime import datetime, timezone

from view.error_message import ErrorMessageBox


# append / create file
def create_print_file():
    with open(r"C:\Users\CM\Desktop\test\data.txt", 'a+'):
        return


def overwrite_to_file():
    with open(r"C:\Users\CM\Desktop\test\data.txt", 'w+') as f:
        data = input("Enter line to write to file: ")
        f.write(data)


def append_to_file():
    with open(r"C:\Users\CM\Desktop\test\data.txt", 'a+') as f:
        data = input("Enter line to append to file: ")
        f.writelines("\n" + data)


def print_file_data():
    with open(r"C:\Users\CM\Desktop\test\data.txt", "r+") as f:
        data = f.read()
        print(data)


def print_files_in_directory(path):
    # import pathlib.Path for Path()
    entry_list = Path(path)  # or os.scandir() syntax delta
    for entry in entry_list.iterdir():  # use .iterdir() on object returned by Path()
        print(entry.name)
    return entry_list


def print_subdirectories_in_directory(path):
    entry_list = Path(path)
    for entry in entry_list.iterdir():
        if entry.is_dir():
            print(entry.name)


def print_last_modified_in_directory(path):
    with os.scandir(path) as files:
        for file in files:
            info = file.stat()
            d = datetime.fromtimestamp(info.st_mtime, tz=timezone.utc)
            print(f"File: {file.name} LM: {d.strftime('%d %b %Y')}")

def create_directory(path):
    try:
        my_path = Path(path)
        my_path.mkdir(parents=True, exist_ok=False)  # can add file exists handling
    except FileExistsError as e:
        print("Cannot create file: " + str(e.strerror))

# will replace destination file if already exists
# check destination beforehand
# def relocate_file(original_path, new_path, collisionLimit = 50):
#     destination_path = new_path
#     counter = 1
#     while(True):
#         try:
#             if not os.path.exists(original_path):
#                 pass   # raise exception / notification for missing original path item
#             if os.path.exists(destination_path):
#                 pass   # raise exception for existing file in destination
#             os.replace(original_path, destination_path)
#             return
#         except FileNotFoundError as e:
#             print("File not found: " + str(e.strerror))
#             return
#         except PermissionError as e:
#             destination_path = new_path + "(" + str(counter) + ")"
#             counter += 1
#             if counter >= collisionLimit + 1:
#                 print("Cannot replace file: System has more than 50 files with the same file name\nError Message: " + str(e.strerror))
#                 return
def relocate_file(original_path, new_path, collisionLimit = 50):
    destination_path = new_path
    counter = 1
    while(True):
        try:
            print(f"From {original_path} to {destination_path}")
            os.replace(original_path, destination_path)
        except FileNotFoundError as e:
            return ErrorMessageBox("File Not Found Error", f"This file cannot be found:\n{original_path}", str(e))
        except PermissionError as e:
            destination_path = new_path + "(" + str(counter) + ")"
            counter += 1
            if counter >= collisionLimit + 1:
                return ErrorMessageBox("Permission Error", f"This file already has the same file name:\n{new_path}", str(e))



def copy_file(original_path, new_path, collisionLimit = 50):
    destination_path = new_path
    counter = 1
    while(True):
        try:
            if not os.path.exists(original_path):
                pass   # raise exception / notification for missing original path item
            if os.path.exists(destination_path):
                pass   # raise exception for existing file in destination
            os.replace(original_path, destination_path)
            return
        except FileNotFoundError as e:
            print("File not found: " + str(e.strerror))
            return
        except PermissionError as e:
            destination_path = new_path + "(" + str(counter) + ")"
            counter += 1
            if counter >= collisionLimit + 1:
                print("Cannot replace file: System has more than 50 files with the same file name\nError Message: " + str(e.strerror))
                return

def main():
    relocate_file(r"C:\Users\CM\Downloads\send.png", r"C:\Users\CM\Documents\Tools3")
    # shutil.copy2(r"C:\Users\CM\PycharmProjects\FileManager_test1\icon\refresh.png", r"C:/Users/CM/Documents/Tools3/aa")
    pass



if __name__ == "__main__":
    main()
