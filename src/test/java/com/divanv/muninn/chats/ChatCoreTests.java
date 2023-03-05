package com.divanv.muninn.chats;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;

import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;

public class ChatCoreTests {

    @Test
    @DisplayName("Given a simple text message, the supplied filter is called")
    public void testSimpleMessageSend() {
        // arrange

        var chatCore = new ChatCore();
        var spy = Mockito.spy(chatCore);


        var requestMessage = new RequestMessage("Hello", "1");

        // act
        chatCore.sendMessage(requestMessage);


        // assert

        // expect chatCore.respond to have been called
    }
}
