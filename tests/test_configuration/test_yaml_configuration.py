import os
from pathlib import PurePath
import pathlib

from digitalpy.core.digipy_configuration.impl.yaml_configuration import (
    YamlConfiguration,
)
from digitalpy.testing.facade_utilities import test_environment


def test_load_single_section_configuration(test_environment):
    # Arrange
    _, _, _ = test_environment
    configuration = YamlConfiguration(
        str(PurePath(__file__).parent / "test_configuration_resources")
    )
    configuration.add_configuration("single_section_config.yml")
    assert configuration is not None
    assert list(configuration.get_sections()) == ["Section1"]
    assert configuration.get_value("key1", "Section1") == "value1"
    assert configuration.get_value("key2", "Section1") == "value2"
    assert configuration.get_value("key3", "Section1") == "value3"


def test_add_multi_section_configuration(test_environment):
    # Arrange
    _, _, _ = test_environment
    configuration = YamlConfiguration(
        str(PurePath(__file__).parent / "test_configuration_resources")
    )

    # Act
    configuration.add_configuration("multi_section_config.yml")

    # Assert
    assert list(configuration.get_sections()) == ["Section1", "Section2"]
    assert configuration.get_value("key1", "Section1") == "value1"
    assert configuration.get_value("key2", "Section1") == "value2"
    assert configuration.get_value("key1", "Section2") == "value3"
    assert configuration.get_value("key2", "Section2") == "value4"  # Arrange

def test_get_configurations(test_environment):
    # Arrange
    _, _, _ = test_environment
    configuration = YamlConfiguration(
        str(PurePath(__file__).parent / "test_configuration_resources")
    )
    configuration.add_configuration("single_section_config.yml")
    configuration.add_configuration("multi_section_config.yml")

    # Act
    configurations = configuration.get_configurations()

    # Assert
    assert len(configurations) == 2
    assert any(config.path.endswith("single_section_config.yml") for config in configurations)
    assert any(config.path.endswith("multi_section_config.yml") for config in configurations)

def test_get_sections(test_environment):
    # Arrange
    _, _, _ = test_environment
    configuration = YamlConfiguration(
        str(PurePath(__file__).parent / "test_configuration_resources")
    )
    configuration.add_configuration("single_section_config.yml")
    configuration.add_configuration("multi_section_config.yml")

    # Act
    sections = configuration.get_sections()

    # Assert
    assert len(sections) == 2
    assert "Section1" in sections
    assert "Section2" in sections

def test_has_section(test_environment):
    # Arrange
    _, _, _ = test_environment
    configuration = YamlConfiguration(
        str(PurePath(__file__).parent / "test_configuration_resources")
    )
    configuration.add_configuration("single_section_config.yml")
    configuration.add_configuration("multi_section_config.yml")

    # Act & Assert
    assert configuration.has_section("Section1") is True
    assert configuration.has_section("Section2") is True
    assert configuration.has_section("Section3") is False

def test_get_section(test_environment):
    # Arrange
    _, _, _ = test_environment
    configuration = YamlConfiguration(
        str(PurePath(__file__).parent / "test_configuration_resources")
    )
    configuration.add_configuration("single_section_config.yml")
    configuration.add_configuration("multi_section_config.yml")

    # Act
    section1 = configuration.get_section("Section1")
    section2 = configuration.get_section("Section2")

    # Assert
    assert section1 == {
        "key1": "value1",
        "key2": "value2",
        "key3": "value3"
    }
    assert section2 == {
        "key1": "value3",
        "key2": "value4"
    }

def test_has_value(test_environment):
    # Arrange
    _, _, _ = test_environment
    configuration = YamlConfiguration(
        str(PurePath(__file__).parent / "test_configuration_resources")
    )
    configuration.add_configuration("single_section_config.yml")
    configuration.add_configuration("multi_section_config.yml")

    # Act & Assert
    assert configuration.has_value("key1", "Section1") is True
    assert configuration.has_value("key2", "Section1") is True
    assert configuration.has_value("key3", "Section1") is True
    assert configuration.has_value("key1", "Section2") is True
    assert configuration.has_value("key2", "Section2") is True
    assert configuration.has_value("key3", "Section2") is False

def test_get_value(test_environment):
    # Arrange
    _, _, _ = test_environment
    configuration = YamlConfiguration(
        str(PurePath(__file__).parent / "test_configuration_resources")
    )
    configuration.add_configuration("single_section_config.yml")
    configuration.add_configuration("multi_section_config.yml")

    # Act & Assert
    assert configuration.get_value("key1", "Section1") == "value1"
    assert configuration.get_value("key2", "Section1") == "value2"
    assert configuration.get_value("key3", "Section1") == "value3"
    assert configuration.get_value("key1", "Section2") == "value3"
    assert configuration.get_value("key2", "Section2") == "value4"

def test_get_boolean_value(test_environment):
    # Arrange
    _, _, _ = test_environment
    configuration = YamlConfiguration(
        str(PurePath(__file__).parent / "test_configuration_resources")
    )
    configuration.add_configuration("complex_config.yml")

    # Act & Assert
    assert configuration.get_boolean_value("key1", "SectionX") is True
    assert configuration.get_boolean_value("key2", "SectionX") is False

def test_get_directory_value(test_environment):
    # Arrange
    _, _, _ = test_environment
    configuration = YamlConfiguration(
        str(PurePath(__file__).parent / "test_configuration_resources")
    )
    configuration.add_configuration("complex_config.yml")

    # Act
    directory_value = configuration.get_directory_value("key3", "SectionX")

    # Assert
    assert isinstance(directory_value, pathlib.Path)
    assert directory_value == pathlib.Path("SomePath")

def test_get_file_value(test_environment):
    # Arrange
    _, _, _ = test_environment
    configuration = YamlConfiguration(
        str(PurePath(__file__).parent / "test_configuration_resources")
    )
    configuration.add_configuration("complex_config.yml")

    # Act
    file_value = configuration.get_file_value("key3", "SectionX")

    # Assert
    assert isinstance(file_value, pathlib.Path)
    assert file_value == pathlib.Path(PurePath(__file__).parent, "test_configuration_resources", "SomePath")

def test_get_key(test_environment):
    # Arrange
    _, _, _ = test_environment
    configuration = YamlConfiguration(
        str(PurePath(__file__).parent / "test_configuration_resources")
    )
    configuration.add_configuration("single_section_config.yml")

    # Act
    key = configuration.get_key("value1", "Section1")

    # Assert
    assert key == "key1"

def test_set_value(test_environment):
    # Arrange
    _, _, _ = test_environment
    configuration = YamlConfiguration(
        str(PurePath(__file__).parent / "test_configuration_resources")
    )
    configuration.add_configuration("single_section_config.yml")

    # Act
    configuration.set_value("key1", "newValue1", "Section1")

    # Assert
    assert configuration.get_value("key1", "Section1") == "newValue1"

def test_remove_section(test_environment):
    # Arrange
    _, _, _ = test_environment
    configuration = YamlConfiguration(
        str(PurePath(__file__).parent / "test_configuration_resources")
    )
    configuration.add_configuration("single_section_config.yml")

    # Act
    configuration.remove_section("Section1")

    # Assert
    assert not configuration.has_section("Section1")

def test_remove_key(test_environment):
    # Arrange
    _, _, _ = test_environment
    configuration = YamlConfiguration(
        str(PurePath(__file__).parent / "test_configuration_resources")
    )
    configuration.add_configuration("single_section_config.yml")

    # Act
    configuration.remove_key("key1", "Section1")

    # Assert
    assert not configuration.has_value("key1", "Section1")
    assert configuration.has_value("key2", "Section1")
    assert configuration.has_value("key3", "Section1")

def test_remove_configuration(test_environment):
    # Arrange
    _, _, _ = test_environment
    configuration = YamlConfiguration(
        str(PurePath(__file__).parent / "test_configuration_resources")
    )
    configuration.add_configuration("single_section_config.yml")
    configuration.add_configuration("multi_section_config.yml")

    # Act
    configuration.remove_configuration("single_section_config.yml")

    # Assert
    assert len(configuration.get_configurations()) == 1
    assert not configuration.has_section("Section1")
    assert configuration.has_section("Section2")
    assert configuration.get_value("key1", "Section2") == "value3"
    assert configuration.get_value("key2", "Section2") == "value4"

def test_save_new_configuration_changes(test_environment):
    # Arrange
    _, _, _ = test_environment
    configuration = YamlConfiguration(
        str(PurePath(__file__).parent / "test_configuration_resources")
    )
    configuration.add_configuration("single_section_config.yml")

    # Act
    configuration.set_value("key1", "newValue1", "Section1")
    configuration.save_configuration("persistent_config.yml")

    # Assert
    configuration = YamlConfiguration(
        str(PurePath(__file__).parent / "test_configuration_resources")
    )
    configuration.add_configuration("persistent_config.yml")
    assert configuration.get_value("key1", "Section1") == "newValue1"

    os.remove(str(PurePath(__file__).parent / "test_configuration_resources" / "persistent_config.yml"))

def test_update_saved_configuration_changest(test_environment):
    # Arrange
    _, _, _ = test_environment
    configuration = YamlConfiguration(
        str(PurePath(__file__).parent / "test_configuration_resources")
    )
    configuration.add_configuration("single_section_config.yml")
    configuration.save_configuration("persistent_config.yml")

    # Act
    configuration = YamlConfiguration(
        str(PurePath(__file__).parent / "test_configuration_resources")
    )
    configuration.add_configuration("persistent_config.yml")
    configuration.set_value("key1", "newValue1", "Section1")
    configuration.save_configuration("persistent_config.yml")

    # Assert
    configuration = YamlConfiguration(
        str(PurePath(__file__).parent / "test_configuration_resources")
    )
    configuration.add_configuration("persistent_config.yml")
    assert configuration.get_value("key1", "Section1") == "newValue1"

    os.remove(str(PurePath(__file__).parent / "test_configuration_resources" / "persistent_config.yml"))