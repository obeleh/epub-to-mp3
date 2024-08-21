import os


def get_files_in_folder(directory):
    """Returns a list of all files in the specified directory."""
    files = [f.name for f in os.scandir(directory) if f.is_file()]
    return files