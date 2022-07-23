from re import A, L
from attr import attr
from lxml import etree
from emergency_RI.constants import BASE_OBJECT_NAME

class ParseXMLToModel:
    def __init__(self, domain, type_processing) -> None:
        self.domain = domain
        self.type_processing = type_processing
    
    def instantiate_model(self, type: str):
        return self.domain.create_node(type, BASE_OBJECT_NAME)

    def parse(self, xml: str):
        type = self.type_processing.get_message_from_xml(xml)
        model = self.instantiate_model(type)
        target_xml_to_model = TargetXMLToModel(model, self.domain)
        parser = etree.XMLParser(target = target_xml_to_model)
        model = etree.XML(xml, parser)
        return model
        
class TargetXMLToModel:

    def __init__(self, model, domain):
        self.events = []
        self.model = model
        self.current_model = model
        self.domain = domain

    def start(self, tag: str, attrib: dict):
        if self.current_model.__class__.__name__.lower() != tag.lower():
            self.current_model = getattr(self.current_model, tag)

        for attr_name, attr_val in attrib.items():
            setattr(self.current_model, attr_name, attr_val)

    def end(self, tag):
        self.current_model = self.domain.get_parent(self.current_model)

    def data(self, data):
        setattr(self.current_model, 'INTAG', data)

    def comment(self, text):
        pass

    def close(self):
        return self.model