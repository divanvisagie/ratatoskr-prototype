package com.divanv.muninn.actors.core;

import com.divanv.muninn.AkkaConfiguration;
import com.divanv.muninn.actors.abilities.chatgpt.ChatGptActor;
import com.divanv.muninn.chats.RequestMessage;
import com.divanv.muninn.chats.ResponseMessage;
import com.divanv.muninn.chats.TelegramBotImpl;
import com.divanv.muninn.repositories.ChatLog;
import com.divanv.muninn.repositories.ChatLogRepository;
import com.divanv.muninn.services.ChatLogService;
import org.springframework.context.ApplicationContext;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;

public class ContextSavingActor extends ChildAwareActor {

    private String question;
    private String chatId;
    private String answer;

    public void saveContext() {
        ApplicationContext context = new AnnotationConfigApplicationContext(AkkaConfiguration.class);
        var service = context.getBean(ChatLogService.class);
        var chatLog = new ChatLog(chatId, question, answer);
        service.save(chatLog);
    }

    @Override
    public Receive createReceive() {
        return receiveBuilder()
            .match(RequestMessage.class, requestMessage -> {
                question = requestMessage.getText();
                chatId = requestMessage.getChatId();
                forwardTo(ChatGptActor.class, requestMessage);
            })
            .match(ResponseMessage.class, responseMessage -> {
                answer = responseMessage.getText();
                saveContext();
                forwardTo(MessageResponseActor.class, responseMessage);
            })
            .matchAny(o -> {
                unhandled(o);
            })
            .build();
    }
}
