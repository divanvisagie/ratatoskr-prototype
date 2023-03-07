package com.divanv.muninn.languagemodels;

import java.util.ArrayList;
import java.util.List;

import com.divanv.muninn.repositories.HistoryEntry;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;

import com.theokanning.openai.completion.chat.ChatCompletionRequest;
import com.theokanning.openai.completion.chat.ChatMessage;
import com.theokanning.openai.service.OpenAiService;

import lombok.Getter;
@Getter
public class ChatGptModel implements LanguageModel {

    public static final String USER_ROLE = "user";
    public static final String ASSISTANT_ROLE = "assistant";

    private static final Logger logger = LoggerFactory.getLogger(ChatGptModel.class);

    private OpenAiService service;

    @Value("${openai.token}")
    private String token = System.getenv("OPENAI_API_KEY");

    private String model = "gpt-3.5-turbo";

    private List<ChatMessage> context = new ArrayList<ChatMessage>();

    // constructor
    public ChatGptModel(
            String prompt) {
        var promptMessage = new ChatMessage("system", prompt);
        context.add(promptMessage);

        this.service = new OpenAiService(token);
    }

    @Override
    public LanguageModel setHistory(List<HistoryEntry> history) {

        return this;
    }

    @Override
    public String getAnswer(String question) {
        var questionMessage = new ChatMessage("user", question);
        context.add(questionMessage);

        try {
            var request = ChatCompletionRequest.builder()
                    .model(model)
                    .messages(context)
                    .maxTokens(100)
                    .build();

            var choices = service.createChatCompletion(request).getChoices();
            return choices.get(0).getMessage().getContent();
        } catch (Exception e) {
            logger.error("Error: " + e.getMessage());
            return "";
        }
    }
}
