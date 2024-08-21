# ZManager: the DigitalPy Multiprocessing Architecture

the observable pattern enables a decoupled event based architecture enabling Multicore and Multithreading capabilities.
Potentially can be distributed across nodes. It's based on  ØMQ (ZeroMQ, 0MQ, zmq) that looks like an embeddable networking library but acts like a concurrency framework.
ØMQ  gives DP sockets that carry whole messages across various transports like in-process, inter-process, TCP, and multicast.
DP  uses sockets N-to-N with patterns like pubsub, and request-reply. 
Its asynchronous I/O model gives DigitalPy a scalable multicore applications, built as asynchronous message-processing tasks.

## Process
![image](https://user-images.githubusercontent.com/60719165/232344598-9337857c-c580-4700-bc3a-cb81a66bb5a0.png)



the FTS services collect requests and push them to the Subject / ventilator. 
### the Subject
The subject AKA ventilator is responsible for dispatching events to registered listeners. 
It sends messages containing the payload coming from the  services. In this sense acts like a load balancer.
It uses a ZMQ_PUSH socket to send messages to workers.

### The worker
The workers receive messages from the ventilator, instantiates the required components, do the work, and send the results down the pipe:
 * instantiates all the required components / core
 * routing messages between them
 * and send the results down the pipe.
 * Uses a ZMQ_PUSH socket to send answers to the  Integration Manager.
 * Uses a ZMQ_SUB socket to receive the FINISH message from the Integration Manager.

### The Integration manager
The Integration manager receives all answers from all workers, prints them, and sends a message to the workers to shut down when all tasks are complete.
Uses a ZMQ_PULL socket to receive answers from the workers.
Uses a ZMQ_PUB socket to send the FINISH message to the workers.

## Core
certain component are part of the DP core as shown in this diagram
![image](https://github.com/user-attachments/assets/e29ce140-0c29-49ad-827e-862880e4e1ce)
