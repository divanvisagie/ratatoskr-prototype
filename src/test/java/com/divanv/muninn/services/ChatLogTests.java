package com.divanv.muninn.services;

import com.divanv.muninn.repositories.HistoryEntry;
import com.divanv.muninn.repositories.ChatLogRepository;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;

@SpringBootTest
public class ChatLogTests {

    @Autowired
    private ChatLogRepository chatLogRepository;

    @Autowired
    private ChatLogService chatLogService;

    private void cleanup() {
        chatLogRepository.deleteAll();
    }

    @Test
    @DisplayName("When asked to persist a chat log, persists the chat log")
    public void testChatLogPersists() {
        // arrange
        var chatId = "a1234";
        var message = "test message";
        var chatLog = new HistoryEntry();
        chatLog.question = "test question";
        chatLog.answer = "test answer";
        chatLog.userId = 1L;

        // act
        chatLogService.save(chatLog);

        // assert
        var actual = chatLogRepository.findByUserId(1L);
        assertNotNull(actual);
        assertEquals("test question", actual.get(0).question);
        assertEquals("test answer", actual.get(0).answer);
        chatLogRepository.deleteAll(actual);
    }
}
