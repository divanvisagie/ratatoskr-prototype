package com.divanv.muninn.languagemodels;

import com.theokanning.openai.completion.chat.ChatMessage;

import lombok.Getter;

public class ChatLog {

    @Getter
    public String question;

    @Getter
    public String answer;

    // constructor
    public ChatLog(String question, String string) {
        this.question = question;
        this.answer = string;
    }

    public QuestionAnswerPair convertToChatMessages() {
        var questionMessage = new ChatMessage(ChatGptModel.USER_ROLE, question);
        var answerMessage = new ChatMessage(ChatGptModel.ASSISTANT_ROLE, answer);

        return new QuestionAnswerPair(questionMessage, answerMessage);
    }
}
