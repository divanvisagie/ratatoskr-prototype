from transformers import pipeline

# Load the QA model
qa_model = pipeline("question-answering")

# Input text and question
text = "John is a software engineer who lives in New York City. He loves to travel and play basketball."
question = "Where does John live?"

# Predict the answer
answer = qa_model({
    "question": question,
    "context": text
})

# Print the answer
print(answer["answer"])
# Output: 'New York City'
