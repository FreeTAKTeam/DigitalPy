# ZManager: the DigitalPy Multiprocessing Architecture

the observable pattern enables a decoupled event based architecture enabling Multicore and Multithreading capabilities.
Potentially can be distributed across nodes. It's based on  ØMQ (ZeroMQ, 0MQ, zmq) that looks like an embeddable networking library but acts like a concurrency framework.
ØMQ  gives DP sockets that carry whole messages across various transports like in-process, inter-process, TCP, and multicast.
DP  uses sockets N-to-N with patterns like pubsub, and request-reply. 
Its asynchronous I/O model gives DigitalPy a scalable multicore applications, built as asynchronous message-processing tasks.

## Process
![image](https://user-images.githubusercontent.com/60719165/232344598-9337857c-c580-4700-bc3a-cb81a66bb5a0.png)



the FTS services collect requests and push them to the Subject / ventilator. 

### The Subject
The Subject, also known as the Ventilator, is responsible for dispatching events to registered workers or listeners. It acts as a load balancer, distributing the payloads it receives from services to multiple workers.

> [!Tip]: The Subject uses a ZMQ_PUSH socket to send messages to the workers.

### The Worker
The Workers receive messages from the Subject and process them. After processing, workers send the results back to the Integration Manager. The workers perform the following tasks:
* Instantiate required components and core modules.
* Route messages between components.
* Send results to the integration manager once processed.

### The Integration Manager
The Integration Manager is the beating heart of the ZManager. It is the single publisher for all messages which can then be subscribed to by any component or service. For this reason the integration manager has practically no logic, it simply publishes messages to the correct topics.

> [!NOTE]: No component, n'or service should ever publish a message directly to the integration manager. All messages should be sent to the integration manager via the subject or other supporting digitalpy infrastructure.

# Topic System

The Topic System defines the structure and flow of message passing between the various components.

## Action Key
The Action Key is a string used to define and route messages between components. In DigitalPy, the action key follows the format:

```ini
Sender?Context@Decorator?Action
```

Where:
* **Sender**: The name of the component or service sending the message.
* **Context**: The context for the message, used to route it to the correct component and define the flow.
* **Decorator** (optional): Used to define special behavior for message routing. The decorator is optional.
* **Action**: The specific action being performed.

## Flow
A flow defines a sequence of actions that should be executed concurrently. Below is an example of a flow definition:

```ini
[IAMConnection]
?IAMConnection?Push
Subject?IAMConnection?Connection
??done
```
1. The Subject service receives a push action.
2. The Subject service sends the next action to the IAM Component.
3. The IAM Component sends a done action to the Integration Manager.

## Decorators
Decorators define special behaviors for message routing in the system. The following decorators are available:

### **PUBLISH** 
The PUBLISH decorator is used to send a message to the Integration Manager, which manages the flow of messages between components.

### **ASYNC**
The ASYNC decorator is used to send a message asynchronously. It is used when the next step in the flow should be initiated by an external process, rather than immediately after the previous action. This decorator is particularly useful for tasks where the result may not be immediately available.

> [!NOTE]
> This only applies to actions that are apart of a flow.

> [!CAUTION]
> This function isn't fully implemented for components yet.

An example of a message with a decorator is in the service management core service:

```ini
[ServiceManagement_GetServiceTopics]
?ServiceManagement_GetServiceTopics?Push
Subject?ServiceManagement__GetServiceTopics@PUBLISH?get_service_topics
?ServiceManagement__GetServiceTopics@ASYNC?get_service_topics_response
??done
```

Explanation:

* The Service Management Core Service first executes the get_service_topics action.
* This action makes a sub-request to the service for topics. The ASYNC decorator is used here to indicate that the service management core should not wait for the response immediately. Instead, the service will send its response when ready.
* The core service stores the current state (via a special key, prev_flow) and continues the flow when the response is received.

## External Action Mapping
Each component in DigitalPy maintains an External Action Mapping file. This file defines the actions that the component can execute.

The mapping is represented as a dictionary where the Action Key is the key, and the value is the function that will be called when the corresponding action is received.

> [!NOTE]
> In the case of the core services, the service will attempt to match the action key to every action key in every flow in order to subscribe to a topic.

Example:
```ini
[actionmapping]
Sender?Context@DECORATOR?Action = myapp.mycomponent.mycomponent_facade.MyComponent.my_method
```
