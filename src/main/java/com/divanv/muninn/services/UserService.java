package com.divanv.muninn.services;

import com.divanv.muninn.repositories.User;
import com.divanv.muninn.repositories.UserRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class UserService {

    private Logger logger = LoggerFactory.getLogger(UserService.class);
    private final UserRepository userRepository;

    @Autowired
    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    public User findByTelegramUsername(String telegramUsername) {
        return userRepository.findByTelegramUsername(telegramUsername);
    }

    public User save(User user) {
        try {
            return userRepository.save(user);
        } catch (Exception e) {
            logger.error("Error saving user: " + e.getMessage());
            return null;
        }
    }
}
