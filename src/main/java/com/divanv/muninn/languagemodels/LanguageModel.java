package com.divanv.muninn.languagemodels;

import java.util.List;

public interface LanguageModel {

    LanguageModel setHistory(List<ChatLog> history);

    String getAnswer(String question);

}