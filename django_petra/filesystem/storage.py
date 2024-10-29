from drf_friend.filesystem.the_disks.local import LocalStorage
from drf_friend.filesystem.the_disks.s3 import S3Storage

class Storage:
    def __init__(self, disk='local'):
        self.disk = disk
        self.local_storage = LocalStorage()
        self.s3_storage = None
        self.set_disk(disk)
        

    def set_disk(self, storage_type):
        if self.disk == 's3':
            self.s3_storage = S3Storage()
        else:
            self.disk = storage_type

    def put(self, path, contents):
        if self.disk == 'local':
            self.local_storage.put(path, contents)
        elif self.disk == 's3':
            self.s3_storage.put(path, contents)

    def get(self, path):
        if self.disk == 'local':
            return self.local_storage.get(path)
        elif self.disk == 's3':
            return self.s3_storage.get(path)

    def delete(self, path):
        if self.disk == 'local':
            self.local_storage.delete(path)
        elif self.disk == 's3':
            self.s3_storage.delete(path)

    def update(self, path, contents):
        if self.disk == 'local':
            self.local_storage.update(path, contents)
        elif self.disk == 's3':
            self.s3_storage.update(path, contents)

    def exists(self, path):
        if self.disk == 'local':
            return self.local_storage.exists(path)
        elif self.disk == 's3':
            return self.s3_storage.exists(path)

    def download(self, source_path, destination_path):
        if self.disk == 'local':
            self.local_storage.download(source_path, destination_path)
        elif self.disk == 's3':
            self.s3_storage.download(source_path, destination_path)

    def url(self, path):
        if self.disk == 'local':
            return self.local_storage.url(path)
        elif self.disk == 's3':
            return self.s3_storage.url(path)

    def temporary_url(self, path, expiration=3600):
        if self.disk == 'local':
            raise ValueError("Temporary URL is not supported for local storage.")
        elif self.disk == 's3':
            return self.s3_storage.temporary_url(path, expiration)

    def all_files(self, directory):
        if self.disk == 'local':
            return self.local_storage.all_files(directory)
        elif self.disk == 's3':
            return self.s3_storage.all_files(directory)

    def directories(self, directory):
        if self.disk == 'local':
            return self.local_storage.directories(directory)
        elif self.disk == 's3':
            return self.s3_storage.directories(directory)

    def append(self, path, contents):
        if self.disk == 'local':
            self.local_storage.append(path, contents)
        elif self.disk == 's3':
            self.s3_storage.append(path, contents)

    def prepend(self, path, contents):
        if self.disk == 'local':
            self.local_storage.prepend(path, contents)
        elif self.disk == 's3':
            self.s3_storage.prepend(path, contents)

    def copy(self, source, destination):
        if self.disk == 'local':
            self.local_storage.copy(source, destination)
        elif self.disk == 's3':
            self.s3_storage.copy(source, destination)

    def move(self, source, destination):
        if self.disk == 'local':
            self.local_storage.move(source, destination)
        elif self.disk == 's3':
            self.s3_storage.move(source, destination)

# Create an instance of the Storage class
storage = Storage()
