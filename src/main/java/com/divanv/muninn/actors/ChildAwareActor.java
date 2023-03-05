package com.divanv.muninn.actors;

import akka.actor.AbstractActor;
import akka.actor.Actor;
import akka.actor.ActorRef;
import akka.actor.Props;

public abstract class ChildAwareActor extends AbstractActor {

    /**
     * Spawns a child and sends a message to it
     * @param message Message to send
     * @param actorClass Class of the child actor
     */
    final protected void forwardTo(Class<? extends Actor> actorClass, Object message) {
        ActorRef childActor = getContext().actorOf(Props.create(actorClass));
        childActor.tell(message, getSelf());
    }
}
