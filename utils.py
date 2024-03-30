import os


def get_file_size_in_kb(size):
    if 0 < size < 1024:
        return '1 KB'
    return str(size // 1024 + 1) + ' KB'


def get_current_directory_name(path):
    path = path.lstrip(os.sep)
    name = path[path.rfind(os.sep)+1:] if os.sep in path else path
    return name
    # if not path:
    #     return ""
    #
    # last_backslash_index = path.rfind("\\")
    # last_forward_slash_index = path.rfind("/")
    # if last_backslash_index != -1:
    #     return path[last_backslash_index + 1:]
    # elif last_forward_slash_index != -1:
    #     return path[last_forward_slash_index + 1:]
    # else:
    #     return ""

def get_parent_directroy_name(path):
    path = path.lstrip(os.sep)  # Get rid of leading "/" if any
    root = path[:path.rfind(os.sep)] if os.sep in path else ""
    return root