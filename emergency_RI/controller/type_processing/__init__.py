from lxml import etree

def get_message_from_xml(xml_str):
    xml_obj = etree.fromstring(xml_str)
    type = xml_obj.get('type')
    return _get_message_from_type(type)

def _get_message_from_type(type):
    message_mapping = {
        "b-a-o-tbl": "emergency"
    }
    return message_mapping.get(type)