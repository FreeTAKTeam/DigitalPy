import io
from digitalpy.core.files.domain.model.file import File


class ReadableFileWrapper(io.IOBase):
    """A wrapper for a file object which exposes the standard io interface for reading and writing files."""

    def __init__(self, file: File):
        self.file = file
        self.file_stream = io.BytesIO(file.contents)

    def read(self, size=-1):
        return self.file_stream.read(size)

    def readline(self, size=-1):
        return self.file_stream.readline(size)

    def readlines(self, hint=-1):
        return self.file_stream.readlines(hint)

    def write(self, data):
        return self.file_stream.write(data)

    def writelines(self, lines):
        return self.file_stream.writelines(lines)

    def seek(self, offset, whence=io.SEEK_SET):
        return self.file_stream.seek(offset, whence)

    def tell(self):
        return self.file_stream.tell()

    def flush(self):
        self.file.contents = self.file_stream.getvalue()

    def close(self):
        return self.file_stream.close()