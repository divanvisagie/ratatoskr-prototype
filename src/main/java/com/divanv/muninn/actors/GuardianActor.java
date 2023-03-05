package com.divanv.muninn.actors;


import com.divanv.muninn.chats.RequestMessage;
import com.divanv.muninn.chats.ResponseMessage;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class GuardianActor extends ChildAwareActor {

    private void respondTo(String chatId, String with) {
        var res = new ResponseMessage(with, chatId);
        forwardTo(MessageResponseActor.class, res);
    }

    final private Logger logger = LoggerFactory.getLogger(GuardianActor.class);

    @Override
    public Receive createReceive() {
        return receiveBuilder()
            .match(RequestMessage.class, requestMessage -> {
               forwardTo(PingPongActor.class, requestMessage);
            })
            .match(ResponseMessage.class, responseMessage -> {
                respondTo(responseMessage.getChatId(), responseMessage.getText());
            })
            .matchAny(o -> {
                unhandled(o);
                logger.error("Got an unknown message");
            })
            .build();
    }
}
