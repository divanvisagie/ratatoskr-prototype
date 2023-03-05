package com.divanv.muninn.repositories;

import org.springframework.data.mongodb.repository.MongoRepository;

import java.util.List;

public interface UserRepository extends MongoRepository<User, Long> {
    User findByTelegramUsername(String telegramUsername);
}
