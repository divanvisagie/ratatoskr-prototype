package com.divanv.muninn.services;


import com.divanv.muninn.repositories.ChatLog;
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

    public void save(ChatLog chatLog) {
        chatLogRepository.save(chatLog);
    }

}
