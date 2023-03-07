package com.divanv.muninn.repositories;

import com.divanv.muninn.languagemodels.ChatGptModel;
import com.divanv.muninn.languagemodels.QuestionAnswerPair;
import com.theokanning.openai.completion.chat.ChatMessage;

import jakarta.persistence.*;
import lombok.Data;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.annotation.LastModifiedDate;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import java.util.Date;

@Data
@Entity(name = "history")
@EntityListeners(AuditingEntityListener.class)
public class HistoryEntry {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    public Long id;

    @Column(name = "user_id")
    public  Long userId;

    public String question;

    public String answer;

    @Column(name = "answered_by")
    public String answeredBy;

    @CreatedDate
    @Column(name = "created_at", updatable = false)
    @Temporal(TemporalType.TIMESTAMP)
    public Date createdAt;

    @LastModifiedDate
    @Version
    @Column(name = "updated_at")
    @Temporal(TemporalType.TIMESTAMP)
    public Date updatedAt;

    public QuestionAnswerPair convertToChatMessages() {
        var questionMessage = new ChatMessage(ChatGptModel.USER_ROLE, question);
        var answerMessage = new ChatMessage(ChatGptModel.ASSISTANT_ROLE, answer);

        return new QuestionAnswerPair(questionMessage, answerMessage);
    }
}
