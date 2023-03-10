package com.divanv.muninn.repositories;

import com.divanv.muninn.languagemodels.ChatGptModel;
import com.divanv.muninn.languagemodels.QuestionAnswerPair;
import com.theokanning.openai.completion.chat.ChatMessage;

import lombok.Data;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.annotation.Id;
import org.springframework.data.annotation.LastModifiedDate;
import org.springframework.data.mongodb.core.mapping.Document;

import java.util.Date;

@Data
@Document(collection = "history")
public class HistoryEntry {

    @Id
    public String id;

    public  String userId;

    public String question;

    public String answer;

    public String answeredBy;

    @CreatedDate
    public Date createdAt;

    @LastModifiedDate
    public Date updatedAt;

    public QuestionAnswerPair convertToChatMessages() {
        var questionMessage = new ChatMessage(ChatGptModel.USER_ROLE, question);
        var answerMessage = new ChatMessage(ChatGptModel.ASSISTANT_ROLE, answer);

        return new QuestionAnswerPair(questionMessage, answerMessage);
    }
}
