# DigitalPy
A framework to support digital engineering in the python language

## introduction
The Digital Architecture Framework (DAF) Metamodel is a UML profile which defines the notation for all elements used in the different stages of an organization life cycle to support the concept of Digital Engineering (DE). from the requirement to the application. Chronos is made to be used within a Model Driven Enterprise approach (MDE).
The aim of the DE is to create a *Digital Twin* of an organization or domain, by holding the all knowledge of the enterprise in an Authoritate Source of Thruth (ASoT)
The products of this knowledge (text documents, code configuration, deployment files, etc.) are generated from the model rather that produced, managed and stored separately.

To be able to transform this abstract model in running code the support of a special class of frameworks is required, this is called Aphodite (Alfa). 
DigitalPy is a Python framework that implements the  Aphrodite 2.0 specifications.

## Goal of  DigitalPy

A software frameworks consists of frozen spots and hot spots. On the one hand, frozen spots define the overall architecture of a software system, that is to say its basic components and the relationships between them. These remain unchanged (frozen) in any instantiation of the application framework. On the other hand, hot spots represent those parts where the programmers using the framework add their own code to add the functionality specific to their own project.
Source http://en.wikipedia.org/wiki/Software_framework 
![image](https://user-images.githubusercontent.com/60719165/201929029-44ec83b7-870a-4baa-bc8e-50e46f558a2e.png)

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
* Encapsulation: Alpha  binds data and attributes or methods and data members in classes
* Inheritance: Alpha allocated features to super classes that can be  inherited from children classes
* Polymorphism: Alpha describe objects with polymorphic charatteristics.

provides a  way to describes concepts like “Domain Object”, Services , View . See also the MVC point below.


## Component Architecture
Aphrodite 1.0 describes a monolithic architecture, the 2.0 specs introduces the concept of Component Architecture. 

### Components features
 * Independent − Components are designed to have minimal dependencies on other components thanks to the DigitalPy routing system.
 * Reusability − Alfa Components are designed to be reused in different situations in different applications. However, some components may be designed for a specific task.
 * Replaceable − Alfa Components may be substituted with other similar components.
 * Not context specific − Alfa Components are designed to operate in different environments and contexts and can be deployed anywhere.
 * Encapsulated −  A component depicts a Facade, which allow the caller to use its functionality, and do not expose details of the internal processes or any internal variables or state.
 * Deployability - Alfa Components can de deployed at runtime, registering themselves to the application core. 

![image](https://user-images.githubusercontent.com/60719165/201923460-71da92c0-f685-4f44-aa19-8dc53fe0119c.png)

The aim of a DigitalPy is to define all the frozen spots, so that is hot spot can be gnerated from the ASOT.
While DigitalPy is well suited for Digital Enginering, there are no dependencies with the ASoT or the DAF Generator (DAFGen) that are mainatined in separated project. 

## package dependencies
![image](https://user-images.githubusercontent.com/60719165/201922228-a4a7842c-8425-437f-be1c-884ec8c852d1.png)

## component Architecture

![image](https://user-images.githubusercontent.com/60719165/201922624-5bcfbda3-8267-4f07-8200-4198db6b8589.png)







