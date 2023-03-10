package com.divanv.muninn.actors.abilities.chatgpt;

import com.divanv.muninn.actors.abilities.AbilityActor;
import com.divanv.muninn.chats.ResponseMessage;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.divanv.muninn.chats.RequestMessage;
import com.divanv.muninn.languagemodels.ChatGptModel;

public class ChatGptActor extends AbilityActor {

    private Logger logger = LoggerFactory.getLogger(ChatGptActor.class);
    public ChatGptActor() {
        super();
        description = "Answers user questions directly";
    }

    private String prompt = "You are Muninn, a large language model trained by OpenAI. You answer questions and when the user asks code questions, you will answer with code examples in markdown format.";

    private void processRequest(RequestMessage requestMessage) {
        logger.info("Processing request");

        ChatGptModel model = new ChatGptModel(prompt);

        String question = requestMessage.getText();

        logger.info("Sending question to model", question);
        String answer = model.getAnswer(question);

        var responseMessage = new ResponseMessage(answer, requestMessage.getChatId());
        sender().tell(responseMessage, self());
    }

    @Override
    public Receive createReceive() {
        return receiveBuilder()
                .match(RequestMessage.class, message -> {
                    processRequest(message);
                })
                .matchAny(o -> {
                    unhandled(o);
                    logger.error("Got an unknown message type", o);
                })
                .build();
    }
}
