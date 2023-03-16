# System Overview

```mermaid
sequenceDiagram
    actor User

    participant Telegram

    box Muninn
    participant message_handler
    participant Context Saving Capability
    participant Switch Capability
    participant Chosen Capability
    participant History Repository
    end
   

    User->>Telegram: Text Message
    activate User

    activate Telegram
    Telegram->>message_handler: User message

    activate message_handler
    message_handler->>Context Saving Capability: User Message

    activate Context Saving Capability
    Context Saving Capability->>Switch Capability: User message

    activate Switch Capability
    Switch Capability->>Switch Capability: Picks filter to forward to
    Switch Capability->>Chosen Capability: User Message

    activate Chosen Capability
    Chosen Capability->>Switch Capability: Response
    deactivate Chosen Capability
    
    Switch Capability->>Context Saving Filter: Response
    deactivate Switch Capability
 
    Context Saving Capability->>History Repository: Save Question and Answer
    Context Saving Capability->>message_handler: Response
    deactivate Context Saving Capability

    message_handler->>Telegram: Response
    deactivate message_handler
    

    Telegram->>User: Response
    deactivate Telegram
    deactivate User

```

## Capabilities

Once the message has been received from a bot interface such as the Telegram library, it is then transformed to a `RequestMessage`. These messages are then passed between a special type of class called a [`Capability`](../filters/filter_types.py). Capabilities either process a message and return a `ResponseMessage`, or pass the message on to another `Filter`, which will then return an `ResponseMessage` back to its caller once it is done.

Capabilities implement an interface that allow the system to treat them all the same way. All capabilities need to provide the following functionality 

### `description`
Since we are dealing with a system that fundamentally runs off of language models, one feature is that a filter can use the description of another filter to help it decide what to do. For example, if a filter is trying to decide whether to process a message, it can use the description of another filter to help it decide. For this to work filters need to provide a description of what they do.

### `relevance_to`
A capability can implement this method to inform the system how relevant it is to a particular message. This is especially useful for filters that are waiting for a user response and may want to make themselves prioritised over other filters in certain situations. 

### `apply`
This is the main method of a capability. It takes a `RequestMessage` and returns a `ResponseMessage`. The text of both the `RequestMessage` and the `ResponseMessage` are then saved by the Context Saving Capability and passed back to the bot interface.


# Performance considerations
One potential improvement would be to use the actor model for filters. Possible implementations in Python include Pykka and [Ray](https://docs.ray.io/en/latest/ray-core/actors.html). 

