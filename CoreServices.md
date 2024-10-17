## What is a core service?
A core service is a special category of service within the **digitalpy** application. These services operate as threads, do not expose any networks, and are solely defined by the core digitalpy system. Unlike other services, core services cannot be extended or modified externally. Their primary purpose is to monitor, manage, and support other core functionalities of the digitalpy platform.

## Current Core Services
This section outlines the core services currently implemented in digitalpy.

* **Service Management Core Service**: This service is responsible for overseeing and managing all other running services in digitalpy.

## Communication With Core Services
Core services interact with other components via messages sent through the [Integration Manager](zmanager.md###The-Integration-Manager). To communicate with a core service, messages should utilize the PUBLISH decorator. This ensures that messages are properly routed to the core service for handling.

An example flow for starting a service is shown below:
```ini
[ServiceManagement_StartService]
?ServiceManagement_StartService?Push # subject receives push action
Subject?ServiceManagement__StartService@PUBLISH?start_service # subject sends next action directly to integration manager
??done # core services publishes done to integration manager
```
Explanation of the Flow:
1. The API triggers an action (e.g., starting a service).
2. The action is passed to the Subject, which forwards it to the Integration Manager.
3. The Integration Manager sends the message to the Service Management Core Service for processing.
4. After completing the requested task, the Service Management Core Service notifies the Integration Manager.
5. The Integration Manager returns the result to the API.

This communication pattern ensures that core services can manage service-related tasks effectively while maintaining the decoupling of components.
