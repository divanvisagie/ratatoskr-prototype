package com.divanv.muninn.chats;

public class ResponseMessage {
    private String text;
    private String chatId;

    public String getChatId() {
        return chatId;
    }

    public String getText() {
        return text;
    }

    public ResponseMessage(String text, String chatId) {
        this.text = text;
        this.chatId = chatId;
    }
}
