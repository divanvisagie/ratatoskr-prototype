package com.divanv.muninn.actors;


import akka.actor.*;
import com.divanv.muninn.AkkaConfiguration;
import com.divanv.muninn.chats.RequestMessage;
import com.divanv.muninn.chats.ResponseMessage;
import com.divanv.muninn.chats.TelegramBotImpl;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.ApplicationContext;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;
import org.telegram.telegrambots.meta.api.methods.send.SendMessage;
import org.telegram.telegrambots.meta.exceptions.TelegramApiException;

public class SmartSwitchActor extends AbstractActor {

    private Logger logger = LoggerFactory.getLogger(SmartSwitchActor.class);

    private void respondToTelegram(RequestMessage requestMessage, String with) {
        ActorRef childActor = getContext().actorOf(Props.create(TelegramResponderActor.class));
        var res = new ResponseMessage(with, requestMessage.getChatId());
        childActor.tell(res, getSelf());
    }

    @Override
    public Receive createReceive() {
        return receiveBuilder()
            .match(RequestMessage.class, requestMessage -> {
                respondToTelegram(requestMessage, "I am a smart switch");
            })
            .matchAny(o -> {
                unhandled(o);
            })
            .build();
    }
}
