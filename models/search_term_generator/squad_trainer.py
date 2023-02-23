from datasets import load_dataset
from transformers import GPT2Tokenizer, AutoModelForQuestionAnswering, TrainingArguments, Trainer, DataCollatorForLanguageModeling

# Load SQuAD dataset
dataset = load_dataset("squad")

# Load pre-trained GPT-2 model
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = AutoModelForQuestionAnswering.from_pretrained("gpt2")

# Tokenize input and convert to model input format
def tokenize_function(example):
    return tokenizer(
        example["question"],
        example["context"],
        truncation="only_second",
        max_length=512,
        padding="max_length",
    )

tokenized_datasets = dataset.map(tokenize_function, batched=True)
train_dataset = tokenized_datasets["train"]

# Define training arguments
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
)

# Define data collator to group input data into batches
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

# Fine-tune model on SQuAD dataset using Trainer class
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    data_collator=data_collator,
    prediction_loss_only=True,
)

trainer.train()
