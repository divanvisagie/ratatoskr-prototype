package com.divanv.muninn.actors;

import akka.actor.AbstractActor;
import com.divanv.muninn.chats.RequestMessage;
import com.divanv.muninn.chats.ResponseMessage;

public class PingPongActor extends AbstractActor {

        @Override
        public Receive createReceive() {
            return receiveBuilder()
                .match(RequestMessage.class, s -> {
                    var responseMessage = new ResponseMessage("Pong", s.getChatId());
                    sender().tell(responseMessage, self());
                })
                .matchAny(o -> {
                    sender().tell(o, self());
                })
                .build();
        }
}
