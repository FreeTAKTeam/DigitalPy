from re import A
from attr import attr
from lxml import etree

class ParseXMLToModel:
    def __init__(self) -> None:
        self.target_xml_to_model = TargetXMLToModel()

    def parse(self, xml: str):
        parser = etree.XMLParser(target = self.target_xml_to_model)
        model = etree.XML(xml, parser)

class TargetXMLToModel:

    def __init__(self, model):
        self.events = []
        self.model = model
        self.current_model = model

    def start(self, tag, attrib):
        if self.current_model.__class__.__name__ != tag:
            self.parent_model = self.current_model
            self.current_model = getattr(self.current_model, tag)

        for attr_name, attr_val in attrib.items():
            setattr(self.current_model, attr_name, attr_val)

    def end(self, tag):
        pass

    def data(self, data):
        setattr(self.current_model, 'INTAG', data)

    def comment(self, text):
        pass

    def close(self):
        return self.model