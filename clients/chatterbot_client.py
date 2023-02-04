from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

# Create a new ChatBot instance
chatbot = ChatBot("QA Bot")

# Train the chatbot on the English corpus
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.english")

# Ask the chatbot a question
response = chatbot.get_response("Where does John live?")

# Print the chatbot's response
print(response)
# Output: New York City
