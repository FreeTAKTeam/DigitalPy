from pathlib import Path
from typing import Union
from digitalpy.core.files.domain.builder.file_builder import FileBuilder

from digitalpy.core.files.persistence.file import File as DBFile


class FileBuilderImpl(FileBuilder):
    """Builds a File object"""

    def add_object_data(
        self, mapped_object: Union[bytes, str, DBFile, Path], protocol=None
    ):
        super().add_object_data(mapped_object)
        if isinstance(mapped_object, Path):
            self._add_path_object_data(mapped_object)

    def _add_path_object_data(self, path: Path):
        self.result.path = path
        self.result.permissions = path.stat().st_mode
        self.result.size = path.stat().st_size
        self.result.name = path.name
        self.result.contents = path.read_bytes()
