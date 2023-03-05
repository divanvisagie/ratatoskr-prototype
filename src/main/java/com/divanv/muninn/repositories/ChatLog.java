package com.divanv.muninn.repositories;

import com.divanv.muninn.languagemodels.ChatGptModel;
import com.divanv.muninn.languagemodels.QuestionAnswerPair;
import com.theokanning.openai.completion.chat.ChatMessage;

import lombok.Getter;
import lombok.Setter;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

@Document
public class ChatLog {

    @Id
    private String id;

    @Getter
    @Setter
    public String question;

    @Getter
    @Setter
    public String answer;

    @Getter
    @Setter
    public String chatId;

    // constructor
    public ChatLog(String question, String string) {
        this.question = question;
        this.answer = string;
    }

    public ChatLog(String chatId, String question, String answer) {
        this.question = question;
        this.answer = answer;
        this.chatId = chatId;
    }

    public QuestionAnswerPair convertToChatMessages() {
        var questionMessage = new ChatMessage(ChatGptModel.USER_ROLE, question);
        var answerMessage = new ChatMessage(ChatGptModel.ASSISTANT_ROLE, answer);

        return new QuestionAnswerPair(questionMessage, answerMessage);
    }
}
