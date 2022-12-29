import os
import time
from datetime import datetime, timedelta
import pickle
from typing import Any, Optional

class FileCache(Cache):
    def __init__(self, cache_dir):
        self.cache_dir = cache_dir
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

    def _get_cache_path(self, section, key):
        return os.path.join(self.cache_dir, f"{section}_{key}")

    def exists(self, section, key):
        return os.path.exists(self._get_cache_path(section, key))

    def get_date(self, section, key):
        cache_path = self._get_cache_path(section, key)
        if not os.path.exists(cache_path):
            return None
        return datetime.fromtimestamp(os.path.getmtime(cache_path))

    def get(self, section, key):
        cache_path = self._get_cache_path(section, key)
        if not os.path.exists(cache_path):
            return None
        with open(cache_path, "rb") as f:
            return f.read()

    def put(self, section: str, key: str, value: Any, lifetime: Optional[int]=None):
            filepath = self._get_filepath(section, key)
            with open(filepath, 'wb') as f:
                pickle.dump(value, f)

    def clear(self, section: str):
        directory = self._get_section_directory(section)
        if os.path.exists(directory):
            for filename in os.listdir(directory):
                filepath = os.path.join(directory, filename)
                os.remove(filepath)

    def clearAll(self):
        if os.path.exists(self.directory):
            for section in os.listdir(self.directory):
                self.clear(section)

    def _get_section_directory(self, section: str) -> str:
        return os.path.join(self.directory, section)

    def _get_filepath(self, section: str, key: str) -> str:
        directory = self._get_section_directory(section)
        if not os.path.exists(directory):
            os.makedirs(directory)
        return os.path.join(directory, key)