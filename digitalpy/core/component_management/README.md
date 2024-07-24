## Overview
The component management component is responsible for managing the lifecycle of components. This consists of the following features:
* Pull Component
  * download a component from a remote datasource as a zip file.
* Discover Component
  * discover zipped components within a specified directory and return their metadata.
* Install Component
  * Install a component which has been downloaded, this includes unzipping the component and registering it within the central configuration.
* Update Component
  * Update a component to a new version, assuming this new version is already downloaded. This will delete the non-persistent data,
  for now the only persistent data is the database.
* Delete Component
  * Delete a components package on the filesystem and remove its records from the configuration.
* Get Component
  * Get a list of the components in the database, these are only the installed components for the time being.
* Register Installed Components
  * This is run at startup to register all the installed component in the central configuration.

## Structure
├───base (the base package containing some empty classes for use by digitalpy internals)
├───configuration (a package containing configuration information)
│   ├───business_rules (a package containing the business rules of the component, unused in component management for now)
│   └───model_definitions (a package containing model definitions in JSON, used to instantiate relationships between model objects dynamically)
├───controllers (a package containing controllers. This forms the basis of the component with all business logic and operations)
│   └───directors (a package containing the directors, used to build complex model objects)
├───domain (a package containing the component's domain objects)
│   ├───builder (a package containing the model object **builders** used to construct the objects)
│   └───model (a package containing the actual model objects)
├───impl (a package containing )
├───logs (a package containing log files)
│   └───ComponentManagement
└───persistence (a package containing persistent data and the sqlalchemy table definitions)
    └───downloads (the folder where downloaded components are stored)

