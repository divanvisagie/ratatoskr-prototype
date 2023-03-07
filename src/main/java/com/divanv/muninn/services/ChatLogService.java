package com.divanv.muninn.services;


import com.divanv.muninn.repositories.HistoryEntry;
import com.divanv.muninn.repositories.ChatLogRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class ChatLogService {
    private final ChatLogRepository chatLogRepository;

    @Autowired
    public ChatLogService(ChatLogRepository chatLogRepository) {
        this.chatLogRepository = chatLogRepository;
    }

    public void save(HistoryEntry chatLog) {
        chatLogRepository.save(chatLog);
    }

}
