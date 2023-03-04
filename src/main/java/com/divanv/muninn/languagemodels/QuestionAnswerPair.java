package com.divanv.muninn.languagemodels;

import com.theokanning.openai.completion.chat.ChatMessage;

public class QuestionAnswerPair {

    private ChatMessage question;

    public ChatMessage getQuestion() {
        return question;
    }

    private ChatMessage answer;

    public ChatMessage getAnswer() {
        return answer;
    }

    public QuestionAnswerPair(ChatMessage question, ChatMessage answer) {
        this.question = question;
        this.answer = answer;
    }
}