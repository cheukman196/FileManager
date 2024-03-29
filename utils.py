def get_file_size_in_kb(size):
    if 0 < size < 1024:
        return '1 KB'
    return str(size // 1024 + 1) + ' KB'
