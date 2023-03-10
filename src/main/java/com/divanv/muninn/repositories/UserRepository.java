package com.divanv.muninn.repositories;

import org.springframework.data.mongodb.repository.MongoRepository;

public interface UserRepository extends MongoRepository<User, String> {
    User findByTelegramUsername(String telegramUsername);
}
