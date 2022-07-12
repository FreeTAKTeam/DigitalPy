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
            self.current_model = getattr(self.current_model, tag)

    def end(self, tag):
        self.events.append("end %s" % tag)

    def data(self, data):
        self.events.append("data %r" % data)

    def comment(self, text):
        self.events.append("comment %s" % text)

    def close(self):
        self.events.append("close")
        return "closed!"