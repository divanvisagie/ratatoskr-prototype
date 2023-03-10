package com.divanv.muninn.services;

import com.divanv.muninn.repositories.HistoryEntry;
import com.divanv.muninn.repositories.ChatLogRepository;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.transaction.annotation.Transactional;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;

@SpringBootTest
@Transactional
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
        chatLog.userId = "mock_user_id";

        // act
        chatLogService.save(chatLog);

        // assert
        var actual = chatLogRepository.findByUserId("mock_user_id").get(0);
        assertNotNull(actual);
        assertEquals("test question", actual.question);
        assertEquals("test answer", actual.answer);
        chatLogRepository.delete(actual);
    }
}
