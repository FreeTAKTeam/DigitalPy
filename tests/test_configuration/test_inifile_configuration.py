import os
from pathlib import PurePath
from digitalpy.core.digipy_configuration.impl.inifile_configuration import InifileConfiguration


def test_load_configuration():
    # Arrange
    configuration = InifileConfiguration(str(PurePath(__file__).parent / "test_configuration_resources"))
    configuration.add_configuration(os.sep+"single_section_config.ini")
    assert configuration is not None
    assert list(configuration.get_sections()) == ["Section1"]
    assert configuration.get_value("key1", "Section1") == "value1"
    assert configuration.get_value("key2", "Section1") == "value2"

def test_load_multisection_configuration():
    # Arrange
    configuration = InifileConfiguration(str(PurePath(__file__).parent / "test_configuration_resources"))
    configuration.add_configuration(os.sep+"multi_section_config.ini")
    assert configuration is not None
    assert list(configuration.get_sections()) == ["Section1", "Section2"]
    assert configuration.get_value("key2", "Section1") == "valueA"
    assert configuration.get_value("key3", "Section1") == "valueB"
    assert configuration.get_value("key2", "Section2") == "value2"
    assert configuration.get_value("key3", "Section2") == "value3"

def test_load_multiple_configurations():
    configuration = InifileConfiguration(str(PurePath(__file__).parent / "test_configuration_resources"))
    configuration.add_configuration(os.sep+"single_section_config.ini")
    configuration.add_configuration(os.sep+"multi_section_config.ini")
    assert configuration is not None
    assert list(configuration.get_sections()) == ["Section1", "Section2"]
    assert configuration.get_value("key1", "Section1") == "value1"
    assert configuration.get_value("key2", "Section1") == "valueA"
    assert configuration.get_value("key3", "Section1") == "valueB"

    assert configuration.get_value("key2", "Section2") == "value2"
    assert configuration.get_value("key3", "Section2") == "value3"

def test_remove_section():
    configuration = InifileConfiguration(str(PurePath(__file__).parent / "test_configuration_resources"))
    configuration.add_configuration(os.sep+"multi_section_config.ini")
    assert configuration is not None
    assert list(configuration.get_sections()) == ["Section1", "Section2"]
    configuration.remove_section("Section1")
    assert list(configuration.get_sections()) == ["Section2"]
    assert configuration.get_value("key2", "Section2") == "value2"
    assert configuration.get_value("key3", "Section2") == "value3"

def test_remove_key():
    configuration = InifileConfiguration(str(PurePath(__file__).parent / "test_configuration_resources"))
    configuration.add_configuration(os.sep+"multi_section_config.ini")
    assert configuration is not None
    assert list(configuration.get_sections()) == ["Section1", "Section2"]
    assert configuration.get_value("key2", "Section1") == "valueA"
    assert configuration.get_value("key3", "Section1") == "valueB"
    configuration.remove_key("key2", "Section1")

    try:
        configuration.get_value("key2", "Section1")
        assert False
    except KeyError:
        assert True
    
    assert configuration.get_value("key3", "Section1") == "valueB"

def test_simple_remove_configuration():
    configuration = InifileConfiguration(str(PurePath(__file__).parent / "test_configuration_resources"))
    configuration.add_configuration(os.sep+"single_section_config.ini")
    configuration.add_configuration(os.sep+"removable_config.ini")
    assert configuration is not None
    assert list(configuration.get_sections()) == ["Section1", "RemoveMe"]
    assert configuration.get_value("key1", "Section1") == "value1"
    assert configuration.get_value("key2", "Section1") == "value2"
    assert configuration.get_value("key", "RemoveMe")
    configuration.remove_configuration(str(PurePath(__file__).parent / "test_configuration_resources" / "removable_config.ini"))

    assert list(configuration.get_sections()) == ["Section1"]
    assert configuration.get_value("key1", "Section1") == "value1"
    assert configuration.get_value("key2", "Section1") == "value2"

def test_remove_modified_configuration():
    configuration = InifileConfiguration(str(PurePath(__file__).parent / "test_configuration_resources"))
    configuration.add_configuration(os.sep+"single_section_config.ini")
    
    configuration.set_value("key1", "value", "Section1")
    configuration.remove_configuration(str(PurePath(__file__).parent / "test_configuration_resources" / "single_section_config.ini"))

    assert list(configuration.get_sections()) == ["Section1"]
    assert configuration.get_value("key1", "Section1") == "value"
