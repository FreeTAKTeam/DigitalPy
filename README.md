## Inheritable Classes for Component Implementation
    * Facade (used to access the internals of any class)
    
    * Default Action Mapper (overriden to expose internal routing)
    
    * Controller (overriden to provide a controller responsible for a specific category of logic)
    
    * Business Rule Controller (overriden to expose a controller which enables specific business rules to controll the calling of controller internals)
    
    * Node (overidden for a specific model object which should be accessible by the domain controller)
    
    * telemetry controller (a controller specifically responsible for handling the instantiation of the implemented telemetry protocols)
    
    * business logic files (a json formatted document containing business rules to be implemented by the business rules controller)
    
    * health check (an interface for a health check to be overriden by each component to expose it's health)

    * metrics controller (a controller responsible for handling the instantiation of the implemented metrics protocol)