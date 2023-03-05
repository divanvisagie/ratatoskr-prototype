package com.divanv.muninn.languagemodels;

import static org.junit.jupiter.api.Assertions.assertEquals;

import com.divanv.muninn.repositories.ChatLog;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

public class ChatLogTests {

    @Test
    @DisplayName("When asked to convert a chat log to chat messages, returns a question answer pair")
    public void testConvertChatLogToChatMessages() {
        // arrange
        var chatLog = new ChatLog("What is the meaning of life?", "42");

        // act
        var actual = chatLog.convertToChatMessages();

        // assert
        assertEquals("user", actual.getQuestion().getRole());
        assertEquals("What is the meaning of life?", actual.getQuestion().getContent());
    }
}
