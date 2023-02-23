"""Custom trainer spat out by ChatGpt"""
from transformers import GPT2Tokenizer, TextDataset, DataCollatorForLanguageModeling, Trainer, TrainingArguments
import torch

# Load tokenizer
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

# Load data
with open('path/to/your/local/dataset.txt', 'r') as f:
    data = f.read()

# Tokenize data
tokenized_data = tokenizer.encode(data)

# Create input sequences
input_ids = []
for i in range(0, len(tokenized_data) - block_size + 1, block_size):
    input_ids.append(tokenizer.build_inputs_with_special_tokens(tokenized_data[i:i+block_size]))

# Create output sequences
output_ids = []
for i in range(block_size, len(tokenized_data), block_size):
    output_ids.append(tokenizer.build_inputs_with_special_tokens(tokenized_data[i:i+block_size]))

# Create dataset
dataset = TextDataset(input_ids=input_ids, output_ids=output_ids)

# Create data collator
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer)

# Create training arguments
training_args = TrainingArguments(
    output_dir='./results',          # output directory
    num_train_epochs=1,              # total number of training epochs
    per_device_train_batch_size=1,   # batch size per device during training
    per_device_eval_batch_size=1,    # batch size for evaluation
    warmup_steps=500,                # number of warmup steps for learning rate scheduler
    weight_decay=0.01,               # strength of weight decay
    logging_dir='./logs',            # directory for storing logs
    logging_steps=10,                # log every N steps
    save_total_limit=2,              # limit the total amount of checkpoints
    save_steps=10_000,               # save checkpoints every N steps
    evaluation_strategy='steps',     # evaluation strategy to adopt during training
    eval_steps=10_000,               # evaluate every N steps
    dataloader_drop_last=True        # drop last incomplete batch if smaller than batch size
)

# Instantiate trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    data_collator=data_collator,
    prediction_loss_only=True
)

# Train model
trainer.train()

# Save model
trainer.save_model('./model')
