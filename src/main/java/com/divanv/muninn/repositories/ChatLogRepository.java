package com.divanv.muninn.repositories;

import org.springframework.data.mongodb.repository.MongoRepository;

import java.util.List;

public interface ChatLogRepository extends MongoRepository<HistoryEntry, String> {
    List<HistoryEntry> findByUserId(String userId);
}
