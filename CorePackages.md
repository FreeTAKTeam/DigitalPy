![image](https://user-images.githubusercontent.com/60719165/232346027-c1d2aa2e-66ea-4e60-bd78-cc3de9b5abc5.png)

DigitalPy core contains the following packages:

# Integration Manager
	The Integration manager receives all answers from all workers, prints them, and sends a message to the workers to shut down when all tasks are complete.
Uses a ZMQ_PULL socket to receive answers from the workers.
Uses a ZMQ_PUB socket to send the FINISH message to the workers.

# Subject
	The subject AKA ventilator is responsible for dispatching events to registered listeners. 
  It sends messages containing the payload coming from the FTS services. In this sense acts like a load balancer.
Uses a ZMQ_PUSH socket to send messages to workers.

# Component Management
This core package contains functions related to Management of components, this includes  discovery, Registration,  installation and de-installation.
Discovery exposes an end point in the rest API that goes trough all the folder in the component and search for non installed ones.
Also contains the interfaces required to be implemented by components.

# DigiPy Configuration
	Provides centralized access to configuration of all components and central core independent from their format (e.g. DB, YAML, INI, .Py)

# Files
	The file package manages the access to the file system including reading and saving different files format such as ini, JSON and YAML

# Health
	the health core package aggregates system information and provides to monitoring services

# IAM
	supports standard authentication and authorization protocols (LDAP, WS-Federation, SAML, OAuth, etc.), for both internal and external applications, 
  API developers and users. 
Two key aspects of securing an application are authentication and authorization. While authentication is the process of verifying the identity of a user, 
authorization means determining if the user is allowed to do what he or she is about to do. That implies that authentication is a precondition for authorization. 
Input validation and filtering is another aspect, which is especially important in web applications
Installation
	Provide ability to create the physical machine, install, upgrade, destroy (kill switch) and de-install current the system

# Logic
	describes the abstract strategy to business logic and it's Implementation

# Main
	the main package is the part of DigitalPy Core that contains the crucial classes of the framework necessary to start a bare bone application

# Network
	the network package features functions providing basic connectivity such as web server, FTP server and so on.

# Persistence
	This core package includes the abstract classes necessary to persist information and the base implementation, additional implementation (e.g. NOSQL) 
  can be added as a component.

# Queries
	Provides abstract access to query the persistency layer. Implementation are specific to application (e.g. GeoQuery)

# Security
	this component is responsible for the creation of Certifications, tokens, passwords and other secure credentials.

# Serialization
	This core package includes the abstract implementation of a serialization and the  the main implementations:
 * JSON
 * XML
 * Protobuff
....

# Service Management
	similarly to component Management, this core function provides the ability to install, deinstall, discovery, 
  start and stop services

# Telemetry
	gathers telemetry information from the different parts of the system and provides access to authorized third parties.
it's organized in two: aggregation and production

# Translation
	translation of messages to different languages.
Internationalization of an application requires to identify all language dependent resources and make them exchangeable 
for the actual localization into a specific language. This includes static and dynamic texts as well as images. 
Since images are referenced by their filename or represented as text (e.g. base64 encoded), it is sufficient to focus on text.

# Validation
The validation component of DigitalPy is responsible for ensuring the accuracy, completeness, and consistency of data within the application. 
It receives data from other components and validates it against predefined rules and criteria. 
The component ensures that data meets specified standards and formats, and that any required data is present and correct. 
The validation component also performs data type validation and cross-field validation to ensure that data is logically consistent. 
If any issues are found, the validation component generates error messages and notifies the appropriate component or user. 
The validation component plays a critical role in maintaining the integrity of the data and ensuring the reliability of the application.	

# ZManager
	this component is an implementation of the communication strategy. It includes all the functions needed to manage ZMQ 

# Util
	the util package contains all the non-specific business or technical capabilities.
e.g. files management
