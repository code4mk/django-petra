import os
import shutil
import mimetypes

from django_petra.path import base_path

class LocalStorage:
    def __init__(self):
        self.base_path = base_path()

    def get_full_path(self, path):
        return os.path.join(self.base_path, 'storage', 'public', path)

    def put(self, path, file):
        full_path = self.get_full_path(path)
        file_content = file.read()
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        # Check if contents is bytes or string
        mode = 'wb' if isinstance(file_content, bytes) else 'w'
        with open(full_path, mode) as file:
            file.write(file_content)

    def get(self, path):
        full_path = self.get_full_path(path)
        with open(full_path, 'rb') as file:
            return file.read()

    def delete(self, path):
        full_path = self.get_full_path(path)
        try:
            os.remove(full_path)
        except FileNotFoundError as e:
            print(f"Error deleting local file: {e}")

    def update(self, path, file):
        self.delete(path)
        self.put(path, file)

    def exists(self, path):
        full_path = self.get_full_path(path)
        return os.path.exists(full_path)

    def download(self, source_path, destination_path):
        full_source_path = self.get_full_path(source_path)
        try:
            shutil.copy(full_source_path, destination_path)
        except FileNotFoundError as e:
            print(f"Error downloading local file: {e}")

    def url(self, path):
        full_path = self.get_full_path(path)
        return f"file://{os.path.abspath(full_path)}"

    def all_files(self, directory):
        full_directory = self.get_full_path(directory)
        try:
            return [os.path.join(full_directory, f) for f in os.listdir(full_directory) if os.path.isfile(os.path.join(full_directory, f))]
        except Exception as e:
            print(f"Error listing all files in local directory: {e}")

    def directories(self, directory):
        full_directory = self.get_full_path(directory)
        try:
            return [d for d in os.listdir(full_directory) if os.path.isdir(os.path.join(full_directory, d))]
        except Exception as e:
            print(f"Error listing directories in local directory: {e}")

    def append(self, path, contents):
        full_path = self.get_full_path(path)
        try:
            with open(full_path, 'a') as file:
                file.write(contents)
        except Exception as e:
            print(f"Error appending to local file: {e}")

    def prepend(self, path, contents):
        full_path = self.get_full_path(path)
        try:
            with open(full_path, 'r') as file:
                old_contents = file.read()
            with open(full_path, 'w') as file:
                file.write(contents + old_contents)
        except Exception as e:
            print(f"Error prepending to local file: {e}")

    def copy(self, source, destination):
        full_source_path = self.get_full_path(source)
        full_destination_path = self.get_full_path(destination)
        try:
            shutil.copy(full_source_path, full_destination_path)
        except Exception as e:
            print(f"Error copying local file: {e}")

    def move(self, source, destination):
        full_source_path = self.get_full_path(source)
        full_destination_path = self.get_full_path(destination)
        try:
            shutil.move(full_source_path, full_destination_path)
        except Exception as e:
            print(f"Error moving local file: {e}")

    def content_type(self, path):
        content_type, _ = mimetypes.guess_type(path)
        if not content_type:
            content_type = 'application/octet-stream'
        return content_type
