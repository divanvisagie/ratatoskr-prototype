package com.divanv.muninn.chats;

import akka.actor.ActorRef;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.telegram.telegrambots.bots.TelegramLongPollingBot;
import org.telegram.telegrambots.meta.api.methods.send.SendMessage;
import org.telegram.telegrambots.meta.api.objects.Update;
import org.telegram.telegrambots.meta.exceptions.TelegramApiException;


public class TelegramBotImpl extends TelegramLongPollingBot {

    @Autowired
    private ActorRef myActor;

    private Logger logger = LoggerFactory.getLogger(TelegramBotImpl.class);
    @Override
    public String getBotUsername() {
        return "Muninn";
    }

    @Override
    public String getBotToken() {
        return System.getenv("TELEGRAM_BOT_TOKEN");
    }

    @Override
    public void onUpdateReceived(Update update) {
        var username = update.getMessage().getFrom().getUserName();
        String chatId = update.getMessage().getChatId().toString();

        if (isStandardTextMessage(update)) {
            SendMessage message = new SendMessage();
            message.setChatId(chatId);
            message.setText("Hello " + username + ", I'm Muninn");

            var requestMessage = new RequestMessage("Got a telegram", chatId);
            myActor.tell(requestMessage, ActorRef.noSender());

            try {
                execute(message);
            } catch (TelegramApiException e) {
                throw new RuntimeException(e);
            }
        }

        update.getMessage().getReplyToMessage();
    }

    private static boolean isStandardTextMessage(Update update) {
        return update.hasMessage() && update.getMessage().hasText();
    }
}
