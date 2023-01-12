# Todo add a class header
	
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Set up database connection and model
engine = create_engine('sqlite:///topic_manager.db')
Base = declarative_base()

# TODO: move this in domain
class Topic(Base):
    __tablename__ = 'topics'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    created_at = Column(DateTime)
    version = Column(Integer)
    
    def __repr__(self):
        return f"<Topic(name='{self.name}', created_at='{self.created_at}')>"

Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

class TopicManagerController:
    
    # Todo enbedd all of this in protected region
    def __init__(self):
        # Retrieve all existing topics from the database
        self.topics = session.query(Topic).all()
    
    def set_topic(self, name):
        # Create a new topic and add it to the database
        new_topic = Topic(name=name, created_at=datetime.datetime.utcnow())
        session.add(new_topic)
        session.commit()
        self.topics.append(new_topic)
    
    def get_topic_list(self):
        # Return a list of all topics
        return [topic.name for topic in self.topics]
        
        
    # Wildcard naming: Topics can include wildcard characters, such as * or ?, which can be used to match multiple topics at once. For example, a subscriber could subscribe to the topic "war/*" to receive all war-related topics, or to the topic "Surface/antisubmarine warfare/?" to receive topics relatives to "antisubmarine warfare" that may or may not be in the specific branch of the hierarchy
    
    def set_HierarchyTopic(self, topic_name: str) -> bool:
        # Split the topic name by '/' to get the hierarchy
        topic_hierarchy = topic_name.split('/')

        # Iterate through the hierarchy and check if there are any wildcard characters
        for i, t in enumerate(topic_hierarchy):
            if t == '*' or t == '?':
                # If a wildcard character is found, set the rest of the hierarchy to None
                topic_hierarchy[i:] = [None] * (len(topic_hierarchy) - i)
                break

        # Create a new Topic object and add it to the session
        new_topic = Topic(name=topic_name)
        self.session.add(new_topic)
        self.session.commit()
        return True
        
    def set_topic_version(self, topic: str, version: int) -> bool:
        """Set the version number for a given topic.
        Versioned naming: Topics can given names that include a version number, which can be incremented whenever the topic's content or meaning changes.  For example "war/GroundTrack/V1" would have a different result that "war/GroundTrack/V2
        
        Args:
            topic: The topic to set the version number for.
            version: The new version number for the topic.
            
        Returns:
            True if the version was successfully set, False otherwise.
        """
        # Check if the topic already exists in the database
        topic_record = self.get_topic(topic)
        if not topic_record:
            return False
        
        # Update the version number in the database
        topic_record.version = version
        self.session.commit()
        return True