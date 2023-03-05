package com.divanv.muninn.services;

import com.divanv.muninn.repositories.User;
import com.divanv.muninn.repositories.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class UserService {
    private final UserRepository userRepository;

    @Autowired
    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    public User findByTelegramUsername(String telegramUsername) {
        return userRepository.findByTelegramUsername(telegramUsername);
    }

    public User save(User user) {
        return userRepository.save(user);
    }
}
