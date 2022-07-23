from emergency_RI.controller import domain
from emergency_RI.controller import type_processing
from .ParseXMLToModel import ParseXMLToModel as __ParseXMLToModel
domain_instance = domain.Domain()

def parse_model_to_xml(model_object)->str:
    pass

def parse_xml_to_model(xml_str):
    return __ParseXMLToModel(domain_instance, type_processing).parse(xml_str)