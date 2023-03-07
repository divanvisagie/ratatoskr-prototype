package com.divanv.muninn.languagemodels;

import static org.junit.jupiter.api.Assertions.assertEquals;

import com.divanv.muninn.repositories.HistoryEntry;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

public class ChatLogTests {

    @Test
    @DisplayName("When asked to convert a chat log to chat messages, returns a question answer pair")
    public void testConvertChatLogToChatMessages() {
        // arrange
        var chatLog = new HistoryEntry();
        chatLog.question = "What is the meaning of life?";
        chatLog.answer = "42";

        // act
        var actual = chatLog.convertToChatMessages();

        // assert
        assertEquals("user", actual.getQuestion().getRole());
        assertEquals("What is the meaning of life?", actual.getQuestion().getContent());
    }
}
