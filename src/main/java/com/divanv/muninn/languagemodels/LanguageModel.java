package com.divanv.muninn.languagemodels;

import com.divanv.muninn.repositories.HistoryEntry;

import java.util.List;

public interface LanguageModel {

    LanguageModel setHistory(List<HistoryEntry> history);

    String getAnswer(String question);

}