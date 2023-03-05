package com.divanv.muninn.services;

import com.divanv.muninn.repositories.User;
import com.divanv.muninn.repositories.UserRepository;

import lombok.Cleanup;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;

@SpringBootTest
// @Transactional
public class UserServiceTests {

    @Autowired
    private UserRepository userRepository;

    private void cleanup() {
        userRepository.deleteAll();
    }

    @Autowired
    private UserService userService;

    @Test
    @DisplayName("When asked to persist a user, persists the user")
    public void testUserPersists() {
        // arrange
        var telegramUsername = "testUser";

        User user = new User();
        user.setTelegramUsername(telegramUsername);

        // act
        userService.save(user);

        // assert
        var actual = userService.findByTelegramUsername(telegramUsername);
        assertNotNull(actual);
        assertEquals(telegramUsername, actual.getTelegramUsername());

        userRepository.delete(actual);
    }

}
