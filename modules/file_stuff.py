import os


def build_file_list_by_path(file_path, file_extensions, file_list, get_subs=False):
    # Iterate over the files in the given file_path
    for file in os.listdir(file_path):
        item_path = os.path.join(file_path, file)

        # Check if the file matches any of the specified extensions
        for extension in file_extensions:
            if file.endswith(extension):
                file_list.append(item_path)

        # If the item is a directory and get_subs is True, recursively build the file list for subdirectories
        if os.path.isdir(item_path) and get_subs:
            build_file_list_by_path(item_path, file_extensions, file_list, True)


class FileList:
    def files_from_path(self, file_path, extensions, list_of_files, recursive=False):
        # Build the file list using the specified file_path, extensions, and recursion settings
        build_file_list_by_path(file_path, extensions, list_of_files, recursive)
        return list_of_files

    def __init__(self, file_path=None, extensions=None, recursive=False):
        self.file_path = file_path
        self.files = []
        self.file_extension_list = []

        # If the file_extensions parameter is not a list, convert it to a list
        if not isinstance(extensions, list):
            self.file_extension_list.append(extensions)
        else:
            self.file_extension_list = extensions

        self.recursive = recursive

        # If a file_path is provided, automatically build the file list
        if file_path is not None:
            self.files_from_path(self.file_path, self.file_extension_list, self.files, recursive)

    def add_extension(self, value):
        self.file_extension_list.append(value)

    def remove_extension(self, value):
        self.file_extension_list.remove(value)

    def clear_files(self):
        self.files = []

    def clear_extensions(self):
        self.file_extension_list = []

    def add_file(self, value):
        # Add a file to the file list
        self.files.append(value)

    def remove_file(self, value):
        # Remove a file from the file list
        self.files.remove(value)

    @property
    def count(self):
        # Get the count of files in the file list
        return len(self.files)

    @count.setter
    def count(self, value):
        # Set the count of files in the file list
        self.count = value
