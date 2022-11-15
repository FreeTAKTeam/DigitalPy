# DigitalPy
A framework to support digital engineering in the Python language

## introduction
The [Digital Architecture Framework](https://github.com/FreeTAKTeam/DigitalArchitectureFramework) (DAF) Metamodel is a modeling language which defines the notation for all elements used in the different stages of an organization life cycle to support the concept of Digital Engineering (DE). from the requirement to the application. DAF isintended to be used within a DE scope.
The aim of the DE is to create a *Digital Twin* of an organization or domain, by holding the all knowledge of the enterprise in an Authoritate Source of Thruth (ASoT)
The products of this knowledge (text documents, code configuration, deployment files, etc.) are generated from the model rather that produced, managed and stored separately.

To be able to transform this abstract model in running code the support of a special class of frameworks is required, this is called Aphodite (Alfa). 
DigitalPy is a Python framework that implements the  Aphrodite 2.0 specifications. Other Aphrodites Frameworks and the original specification  are maintained under the [Olympos MDA](https://sourceforge.net/projects/olympos/) project (e.g. VenusSharp a C# implementation). 
The most notable being the [WCMF](https://wcmf.wemove.com) an Aphrodite framework for PHP.

## Goal of  DigitalPy

Am Aphrodites  frameworks consists of [frozen spots and hot spots](http://en.wikipedia.org/wiki/Software_framework ). On the one hand, frozen spots define the overall architecture of a software system, that is to say its basic components and the relationships between them. These remain unchanged (frozen) in any instantiation of the application framework. On the other hand, hot spots represent those parts where the programmers using the framework add their own code to add the functionality specific to their own project.

![image](https://user-images.githubusercontent.com/60719165/201929029-44ec83b7-870a-4baa-bc8e-50e46f558a2e.png)
The aim of a DigitalPy is to define all the frozen spots, so that is hot spot can be gnerated from the ASOT.
While DigitalPy is well suited for Digital Enginering, there are no dependencies with the ASoT or the DAF Generator ([DAFGen](https://github.com/FreeTAKTeam/FreeTAKModel)) that are maintained as a separated project.

## Aphrodite principles
### KISS Keep It Simple Stupid
This is not about “how easy the Hello World example is” rather “How long you need to understand enough to use it”. 
Design simplicity is a key principle and unnecessary complexity is avoided to the user. DigitalPy  hides the complexity behind a clear defined, simple API.  

### Convention vs Configuration
A lesson learned from “Ruby on rails” in positive and the typical old J2EE application in negative sense.
DigitalPy runs with minimal or no configuration. Even if a configurable entity was not configured, there should be some proper default to attach it with.

### (Good) Object Orientation
DigitalPy follows 
* Abstraction: Alpha abstraction, supports the KISS principle, by hiding internal implementation and showing only the required features or set of services that are offered. 
* Encapsulation: Alpha  binds data and attributes or methods and data members in classes, also implements the Facade structural pattern (see below)
* Inheritance: Alpha allocates features to super classes that can be  inherited from children classes
* Polymorphism: Alpha describe objects with polymorphic charatteristics.

provides a  way to describes concepts like “Domain Object”, Services , View . See also the MVC point below.

## Model-View-Controller
 is an architectural pattern used in software engineering. Successful use of the pattern isolates business logic from user interface considerations, resulting in an application where it is easier to modify either the visual appearance of the application or the underlying business rules without affecting the other.
 
 ### Model
An application is usually based on a domain model that represents the real-world concepts of the domain of interest. In object oriented programming this model is implemented using classes. Depending on the application requirements the instances of some of these classes have to be persisted in a storage to keep the contained data. These classes represent the data model. The classes that provide the infrastructure for storing data form the persistence layer.


![image](https://user-images.githubusercontent.com/60719165/201990851-634ce6ed-f980-426d-95be-4367dc24c0c2.png)
the  dModelclasses  support the ability to Create, read, update and delete (CRUD) tree of elements taking in account the model information.
DigitalPy defines [PersistentObject](https://github.com/FreeTAKTeam/DigitalPy/blob/main/digitalpy/model/persistent_object.py) as base class for persistent domain classes. It mainly implements an unique identifier for each instance (see [ObjectId](https://github.com/FreeTAKTeam/DigitalPy/blob/main/digitalpy/model/object_id.py)), tracking of the persistent state, methods for setting and getting values as well as callback methods for lifecycle events. For the composition of object graphs the derived class Node is used as base class. It implements relation support for persistent objects.

To retrieve persisted objects [PersistenceFacade](https://github.com/FreeTAKTeam/DigitalPy/blob/main/digitalpy/model/persistence_facade.py) is used. The actual operations for creating, reading, updating and deleting objects (e.g. SQL commands) are defined in classes implementing the [PersistenceMapper](https://github.com/FreeTAKTeam/DigitalPy/blob/main/digitalpy/model/persistence_mapper.py) interface (see Data Mapper Pattern). Although not necessary there usually exists one mapper class for each persistent domain class. Mapper classes are introduced to the persistent facade by configuration.

## Modular design
Modular design is a generally recognized “Good Thing(tm)” in software engineering. As in science in general, breaking a problem down to smaller, bite-sized pieces makes it easier to solve. It also allows different people to solve different parts of the problem and still have it all work correctly in the end. Each component is then self-contained and, as long as the interface between different components remains constant, can be extended or even gutted and rewritten as needed without causing a chaotic mess. DigitalPy supports this principle with his component Architecture (see below).

### Component Architecture
Aphrodite 1.0 describes a monolithic architecture, to support a better modular design, the 2.0 specs introduces the concept of Component Architecture. 

### Components features
 * Independent − Alfa Components are designed to have minimal dependencies on other components thanks to the DigitalPy routing system.
 * Reusability − Alfa Components are designed to be reused in different situations in different applications. However, some components may be designed for a specific task.
 * Replaceable − Alfa Components may be substituted with other similar components.
 * Not context specific − Alfa Components are designed to operate in different environments and contexts and can be deployed anywhere.
 * Encapsulated −  A component depicts a Facade, which allow the caller to use its functionality, and do not expose details of the internal processes or any internal variables or state.
 * Deployability - Alfa Components can de deployed at runtime, registering themselves to the application core. 

![image](https://user-images.githubusercontent.com/60719165/201923460-71da92c0-f685-4f44-aa19-8dc53fe0119c.png)

 ## component Architecture

![image](https://user-images.githubusercontent.com/60719165/201922624-5bcfbda3-8267-4f07-8200-4198db6b8589.png)
### Facade
 each component exposes a Facade, that is inheriting from the framework Facade. All the messages are routed trough the facade to the Component Actionmapper that allocates the action to the proper controller as defined in internalActionMapping.ini.

this allows:
 * Isolation: We can easily isolate our code from the complexity of a subsystem.
 * Testing Process: Using Facade Method makes the process of testing comparatively easy since it has convenient methods for common testing tasks.
 * Loose Coupling: Availability of loose coupling between the clients and the Subsystems.
 
 each component exposes a Facade, that is inheriting from the framework Facade. All the messages are routed trough the facade to the Component Actionmapper that allocates the action to the proper controller as defined in internalActionMapping.ini.


## DigitalPy package dependencies
![image](https://user-images.githubusercontent.com/60719165/201922228-a4a7842c-8425-437f-be1c-884ec8c852d1.png)

