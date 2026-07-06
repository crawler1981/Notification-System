```mermaid
sequenceDiagram
    participant Notification
    participant Gateway
    participant Library
    participant Queue(RabbitMQ) 
    participant gRPC

    Gateway ->> Queue : send notification
    Queue ->> Notification : send notification
    Notification ->> Notification : print notification
    
    Gateway ->> gRPC : send notification
    gRPC ->> Library : send notification
    Library ->> Library : print notification
```