from controller import Controller

class Emergency(Controller):
    def __init__(self, ):
        self.emergencies = []

    def accept_visitor(self, visitor):
        pass

    def broadcast_emergencies(self):
        for emergency in self.emergencies:
            self.broadcast_emergency( emergency )
        

    def broadcast_emergency(self, emergency_object):
        pass
