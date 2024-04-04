import os
import re
import shutil
from pathlib import Path

from view.error_message import ErrorMessageBox


def get_file_size_in_kb(size):
    if 0 < size < 1024:
        return '1 KB'
    return str(size // 1024 + 1) + ' KB'


# pass an absolute path, get the file name (name + extensions)
def get_current_directory_name(path):
    path = path.lstrip(os.sep)
    name = path[path.rfind(os.sep) + 1:] if os.sep in path else path
    return name


# pass an absolute path, get the parent directory's path
def get_parent_directory_name(path):
    path = path.lstrip(os.sep)  # remove leading slashes
    root = path[:path.rfind(os.sep)] if os.sep in path else ""
    return root


# moves files from one path to the other
# naming collision: if file names collide, add (1) up to (50) to avoid collision
def relocate_file(original_path, new_path, collisionLimit=50):
    destination_path = new_path
    if not Path(destination_path).exists():
        raise FileNotFoundError(f"Destination folder cannot be found:\n{new_path}")
    if not Path(original_path).exists():
        raise FileNotFoundError(f"Source file cannot be found:\n{original_path}")
    counter = 1
    while (True):
        try:
            os.replace(original_path, destination_path)
            return
        except FileNotFoundError as e:
            return ErrorMessageBox("File Not Found Error", f"File cannot be found.", str(e))
        except PermissionError as e:
            # if duplicate file with same name exists, os.replace raises PermissionError
            # handle file name collision: fileName => fileName(1) => fileName(2)
            destination_path = new_path + os.sep + Path(original_path).stem + "(" + str(counter) + ")" + Path(
                original_path).suffix
            counter += 1
            if counter >= collisionLimit + 1:
                return ErrorMessageBox("Permission Error", f"This file already has the same file name:\n{new_path}",
                                       str(e))
        except Exception as e:
            return ErrorMessageBox("Error", f"Unexpected Error when moving files.", str(e))


# copy files from one path to the other
def copy_file(original_path, new_path, collisionLimit=50):
    if not Path(new_path).exists():
        raise FileNotFoundError(f"Destination folder cannot be found:\n{new_path}")
    if not Path(original_path).exists():
        raise FileNotFoundError(f"Source file cannot be found:\n{original_path}")

    file_type = Path(original_path).suffix
    file_name = Path(original_path).stem
    resultant_file_path_holder = new_path + os.sep + file_name
    resultant_file_path = resultant_file_path_holder + file_type

    counter = 1
    while (True):
        try:
            if os.path.exists(resultant_file_path):
                # shutil.copy2() replaces files with same names, so we manually check to prevent replacement
                # handle file name collision: fileName => fileName(1) => fileName(2)
                resultant_file_path = resultant_file_path_holder + "(" + str(counter) + ")" + file_type
                counter += 1
                if counter >= collisionLimit + 1:
                    return ErrorMessageBox("File Name Error",
                                           f"This file already has the same file name:\n{resultant_file_path_holder}")
        except FileNotFoundError as e:
            return ErrorMessageBox("File Not Found Error", f"File cannot be found.", str(e))
        except PermissionError as e:
            return ErrorMessageBox("Permission Error", f"You don't have write permissions in {new_path}", str(e))
        except Exception as e:
            return ErrorMessageBox("Error", f"Unexpected Error when moving files.", str(e))
        else:
            # if all checks pass, copy file
            return shutil.copy2(original_path, resultant_file_path)

