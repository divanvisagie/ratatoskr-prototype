package com.divanv.muninn.chats;

public class ChatCore {
    public void sendMessage(RequestMessage requestMessage) {
        var responseMessage = new ResponseMessage("Hi", "123");
        respond(responseMessage);
    }

    public void respond(ResponseMessage responseMessage) {
    }
}
