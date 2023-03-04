package com.divanv.muninn.languagemodels;

import static org.junit.jupiter.api.Assertions.fail;

import java.util.ArrayList;
import java.util.List;

import com.divanv.muninn.languagemodels.ChatGptModel;
import com.divanv.muninn.languagemodels.ChatLog;
import com.divanv.muninn.languagemodels.LanguageModel;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import edu.stanford.nlp.util.StringUtils;

public class ChatGptModelTests {

    private static boolean isFuzzyMatch(String s1, String s2, double threshold) {
        int editDistance = StringUtils.editDistance(s1, s2);
        double similarity = 1.0 - ((double) editDistance / (double) Math.max(s1.length(), s2.length()));
        return similarity >= threshold;
    }

    /**
     * Assertion based on how close 2 strings are to each other
     * 
     * @param expected   The string you expect to see
     * @param actual     The string that came from the test
     * @param strictness 0.0 - 1.0, 1.0 being exact match
     */
    private static void assertFuzzyMatch(String expected, String actual, double strictness) {
        boolean isMatch = isFuzzyMatch(expected, actual, strictness);
        if (!isMatch) {
            fail(String.format("Strings are not equal (ignoring case): expected=%s, actual=%s", expected, actual));
        }
    }

    @Test
    @DisplayName("When asked to search for akka documentation, returns concise answer")
    public void testChatGptModelConciseAnswer() {
        // arrange
        var prompt = "You provide search terms tor users to use in a search engine, provide only the search term for the prompt.";
        LanguageModel chatGptModel = new ChatGptModel(prompt);
        List<ChatLog> history = new ArrayList<ChatLog>();

        // act
        String actual = chatGptModel.setHistory(history).getAnswer("Show me the akka documentation");

        // assert
        assertFuzzyMatch("akka documentation", actual, 0.9);
    }
}
