package com.divanv.muninn.actors.core;

import akka.actor.UntypedAbstractActor;
import com.divanv.muninn.AppConfiguration;
import com.divanv.muninn.chats.ResponseMessage;
import com.divanv.muninn.chats.TelegramBotImpl;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.context.ApplicationContext;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;
import org.telegram.telegrambots.meta.api.methods.send.SendMessage;
import org.telegram.telegrambots.meta.exceptions.TelegramApiException;


public class MessageResponseActor extends UntypedAbstractActor {

    private Logger logger = LoggerFactory.getLogger(GuardianActor.class);

    private void replyToTelegram(String messageText, String chatId) {
        ApplicationContext context = new AnnotationConfigApplicationContext(AppConfiguration.class);
        // Telegram bot
        var bot = context.getBean(TelegramBotImpl.class);

        SendMessage message = new SendMessage();
        message.setChatId(chatId);
        message.setText(messageText);
        message.enableMarkdown(true);

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
