package com.divanv.muninn.actors.core;

import com.divanv.muninn.actors.abilities.chatgpt.ChatGptActor;
import com.divanv.muninn.chats.RequestMessage;
import com.divanv.muninn.chats.ResponseMessage;
import com.divanv.muninn.repositories.HistoryEntry;

//@Component
//@Scope(ConfigurableBeanFactory.SCOPE_PROTOTYPE)
public class ContextSavingActor extends ChildAwareActor {

    private String question;
    private String chatId;
    private String answer;

//    @Autowired
//    private ChatLogService chatLogService;

    public void saveContext() {

        var chatLog = new HistoryEntry();
        chatLog.question = question;
        chatLog.answer = answer;
//        chatLogService.save(chatLog);
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
