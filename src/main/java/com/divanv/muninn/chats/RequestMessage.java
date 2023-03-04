package com.divanv.muninn.chats;

public class RequestMessage {
    private String text;

    public String getText() {
        return text;
    }

    public String chatId;

    public String getChatId() {
        return chatId;
    }

    public RequestMessage(String text, String chatId) {
        this.text = text;
        this.chatId = chatId;
    }
}
