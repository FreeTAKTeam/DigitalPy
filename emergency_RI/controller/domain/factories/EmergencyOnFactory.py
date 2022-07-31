from digitalpy.model import event, detail, link, contact, emergency

class EmergencyOnFactory:
    def __init__(self, relationship_definition):
        self.relationship_definition = relationship_definition["EmergencyOn"]
    
    def build(self):
        Event = self.build_objects()
        self.insert_relationships()
        return Event

    def build_objects(self):
        self.Link = self.build_object(link)
        self.Contact = self.build_object(contact)
        self.Emergency = self.build_object(emergency)
        self.Detail = self.build_object(detail, self.Link, self.Contact, self.Emergency)
        self.Event = self.build_object(event, self.Detail)
        return self.Event
    
    def build_object(self, object, *children):
        return object(*children)

    def insert_relationships(self):
        
        event_relationships = self.RelationshipDefinition["event"]
        detail_relationships = event_relationships["children"]["detail"]
        link_relationships = detail_relationships["children"]["link"]
        emergency_relationships = detail_relationships["children"]["emergency"]
        contact_relationships = detail_relationships["children"]["contact"]

        self.insert_relationship(event, event_relationships)
        self.insert_relationship(detail, detail_relationships)
        self.insert_relationship(link, link_relationships)
        self.insert_relationship(emergency, emergency_relationships)
        self.insert_relationship(contact, contact_relationships)
        
    def insert_relationship(self, object, relationship):
        object._add_relationship_definition(relationship)