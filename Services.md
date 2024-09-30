# How to create a service

## Choosing a network

This section will step through how you can go about creating a new service in a digitalpy application. Before you can build your service you need to decide on the network it will listen on. In digitalpy a network can be thought of as the part of the service which reads the data directly from the client and converts it to the container abstraction used by digitalpy. As of v0.13.4 digitalpy only has two networks:
* Flask HTTP Blueprint Network
* TCP Network

For the sake of simplicity we will assume you choose to use the TCP Network in this tutorial.

## Configuring your service

In your object ini file you will add the following section:
```ini
[application_name.service_id]
__class = full.path.to.class.MyService
```

In your configuration ini file you will add the following section:
```ini
[application_name.service_id]
__class = digitalpy.core.service_management.domain.model.service_configuration.ServiceConfiguration
status = STOPPED
name = MyNewService
port = 8443
host = 0.0.0.0
protocol = TCP
```

Next you will add or update the ServiceManagementConfiguration section as follows:
```ini
[ServiceManagementConfiguration]
__class = digitalpy.core.service_management.domain.model.service_management_configuration.ServiceManagementConfiguration
services = [application_name.service_id]
```