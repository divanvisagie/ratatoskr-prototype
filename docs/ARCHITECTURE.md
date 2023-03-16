# System Overview

```mermaid
sequenceDiagram
    actor User

    participant Telegram

    box Muninn
    participant message_handler
    participant Context Saving Filter
    participant Switch Filter
    participant Chosen Filter
    participant History Repository
    end
   

    User->>Telegram: Text Message
    activate User

    activate Telegram
    Telegram->>message_handler: User message

    activate message_handler
    message_handler->>Context Saving Filter: User Message

    activate Context Saving Filter
    Context Saving Filter->>Switch Filter: User message

    activate Switch Filter
    Switch Filter->>Switch Filter: Picks filter to forward to
    Switch Filter->>Chosen Filter: User Message

    activate Chosen Filter
    Chosen Filter->>Switch Filter: Response
    deactivate Chosen Filter
    
    Switch Filter->>Context Saving Filter: Response
    deactivate Switch Filter
 
    Context Saving Filter->>History Repository: Save Question and Answer
    Context Saving Filter->>message_handler: Response
    deactivate Context Saving Filter

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

### `process`
This is the main method of a filter. It takes a `RequestMessage` and returns a `ResponseMessage`. The text of the `ResponseMessage` is then saved by the Context Saving Filter and passed back to the bot interface.


# Performance considerations
One potential improvement would be to use the actor model for filters. Possible implementations in Python include Pykka and [Ray](https://docs.ray.io/en/latest/ray-core/actors.html). 

