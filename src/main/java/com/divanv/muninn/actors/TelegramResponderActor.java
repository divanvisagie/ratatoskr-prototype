package com.divanv.muninn.actors;

import akka.actor.UntypedAbstractActor;
import com.divanv.muninn.AkkaConfiguration;
import com.divanv.muninn.chats.ResponseMessage;
import com.divanv.muninn.chats.TelegramBotImpl;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.ApplicationContext;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;
import org.springframework.stereotype.Component;
import org.telegram.telegrambots.meta.api.methods.send.SendMessage;
import org.telegram.telegrambots.meta.exceptions.TelegramApiException;


public class TelegramResponderActor extends UntypedAbstractActor {

    private Logger logger = LoggerFactory.getLogger(SmartSwitchActor.class);

    private void replyToTelegram(String messageText, String chatId) {
        ApplicationContext context = new AnnotationConfigApplicationContext(AkkaConfiguration.class);
        // Telegram bot
        var bot = context.getBean(TelegramBotImpl.class);

        SendMessage message = new SendMessage();
        message.setChatId(chatId);
        message.setText(messageText);

        try {
            bot.execute(message);
        } catch (TelegramApiException e) {
            throw new RuntimeException(e);
        }

    }

    @Override
    public void onReceive(Object message) throws Throwable, Throwable {

        if (message instanceof ResponseMessage responseMessage) {
            logger.info("Got a response message");
            replyToTelegram(responseMessage.getText(), responseMessage.getChatId());
        } else {
            unhandled(message);
        }
    }
}
