import pytest
import tempfile
from pathlib import Path

from digitalpy.core.files.files_facade import Files
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.zmanager.impl.async_action_mapper import AsyncActionMapper
from digitalpy.core.zmanager.impl.default_action_mapper import DefaultActionMapper
from digitalpy.core.digipy_configuration.impl.inifile_configuration import InifileConfiguration
from digitalpy.core.main.singleton_configuration_factory import SingletonConfigurationFactory
from tests.testing_utilities.facade_utilities import (
    initialize_facade,
    initialize_test_environment,
)

@pytest.fixture
def files_facade():
    request, response, _ = initialize_test_environment()
    
    files_facade: Files = initialize_facade(
        "digitalpy.core.files.files_facade.Files",
        request,
        response,
    )

    return files_facade

@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir

def test_get_or_create_file_creates_new_file(files_facade: Files, temp_dir: tempfile.TemporaryDirectory):
    """Test get_or_create_file creates a new file if it doesn't exist."""
    # Arrange
    file_path = Path(temp_dir) / "test_file.txt"

    # Act
    file_obj = files_facade.get_or_create_file(path=str(file_path), config_loader=None)

    # Assert
    assert file_obj is not None
    assert file_path.exists()
    assert file_obj.path == str(file_path)

def test_get_or_create_file_returns_existing_file(files_facade: Files, temp_dir: tempfile.TemporaryDirectory):
    """Test get_or_create_file returns an existing file."""
    # Arrange
    file_path = Path(temp_dir) / "test_file.txt"
    file_path.touch()  # Create the file

    # Act
    file_obj = files_facade.get_or_create_file(path=str(file_path), config_loader=None)

    # Assert
    assert file_obj is not None
    assert file_path.exists()
    assert file_obj.path == str(file_path)

def test_create_file_creates_new_file(files_facade: Files, temp_dir: tempfile.TemporaryDirectory):
    """Test create_file creates a new file."""
    # Arrange
    file_path = Path(temp_dir) / "test_create_file.txt"

    # Act
    file_obj = files_facade.create_file(path=str(file_path), config_loader=None)

    # Assert
    assert file_obj is not None
    assert file_path.exists()
    assert file_obj.path == str(file_path)

def test_get_file_raises_error_when_not_exists(files_facade: Files, temp_dir: tempfile.TemporaryDirectory):
    """Test get_file raises FileNotFoundError if the file doesn't exist."""
    # Arrange
    file_path = Path(temp_dir) / "non_existent_file.txt"

    # Act & Assert
    with pytest.raises(FileNotFoundError):
        files_facade.get_file(path=str(file_path), config_loader=None)

def test_delete_file(files_facade: Files, temp_dir: tempfile.TemporaryDirectory):
    """Test delete_file removes the specified file."""
        # Arrange
    file_path = Path(temp_dir) / "test_delete_file.txt"
    file_path.touch()  # Create the file
    file_obj = files_facade.get_file(path=str(file_path), config_loader=None)
    file_obj.contents = b"New content"

    # Act
    files_facade.delete_file(client=None, config_loader=None, file=file_obj)

    # Assert
    assert not file_path.exists()

def test_update_file(files_facade: Files, temp_dir: tempfile.TemporaryDirectory):
    """Test update_file writes content to the file."""
    # Arrange
    file_path = Path(temp_dir) / "test_update_file.txt"
    file_path.touch()  # Create the file
    file_obj = files_facade.get_file(path=str(file_path), config_loader=None)
    file_obj.contents = b"New content"

    # Act
    updated_file = files_facade.update_file(file=file_obj, config_loader=None)

    # Assert
    assert updated_file is not None
    assert file_path.exists()
    with open(file_path, "rb") as f:
        assert f.read() == b"New content"
