import os


def get_file_size_in_kb(size):
    if 0 < size < 1024:
        return '1 KB'
    return str(size // 1024 + 1) + ' KB'


def get_current_directory_name(path):
    path = path.lstrip(os.sep)
    name = path[path.rfind(os.sep) + 1:] if os.sep in path else path
    return name


def get_parent_directory_name(path):
    path = path.lstrip(os.sep)  # remove leading slashes
    root = path[:path.rfind(os.sep)] if os.sep in path else ""
    return root
