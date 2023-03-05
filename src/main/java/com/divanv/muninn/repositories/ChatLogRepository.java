package com.divanv.muninn.repositories;

import org.springframework.data.mongodb.repository.MongoRepository;

public interface ChatLogRepository extends MongoRepository<ChatLog, Long> {
}
