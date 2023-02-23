import logging
from transformers import pipeline, set_seed, GPT2LMHeadModel, GPT2Tokenizer
import torch

#MODEL_NAME = "jordiclive/instruction-tuned-gpt-neox-20b"
MODEL_NAME = "gpt2"
#EleutherAI/gpt-j-6B
#facebook/opt-125m

logger = logging.getLogger(__name__)

# Initialize the chat history
history = [
    #"Human: What is the actor library for scala?\nBot: Akka."
    ]
generator = pipeline('text-generation', model=f"{MODEL_NAME}", do_sample=True)

# Define the chatbot logic
def chatbot_response(input_text, history):
    # Concatenate the input text and history list
    input_text = "\n".join(history) + "\nHuman: " + input_text + " Bot: "
    set_seed(32)
    response_text = generator(input_text, max_length=250, num_beams=1, num_return_sequences=1)[0]['generated_text']
    logger.info(response_text)
    # Extract the bot's response from the generated text
    response_text = response_text.split("Bot:")[-1]
    # Cut off any "Human:" or "human:" parts from the response
    response_text = response_text.split("Human:")[0]
    response_text = response_text.split("human:")[0]
    return response_text

def generate_text(input_text, model, tokenizer):
    input_ids = tokenizer.encode(input_text, return_tensors='pt')
    attention_mask = torch.ones(input_ids.shape, dtype=torch.long, device=input_ids.device)
    output = model.generate(input_ids=input_ids, attention_mask=attention_mask, max_length=50, do_sample=True)
    output_text = tokenizer.decode(output[0], skip_special_tokens=True)
    return output_text.strip()


def get_gpt_2_response(input_text):
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    model = GPT2LMHeadModel.from_pretrained('gpt2')
    return generate_text(input_text, model, tokenizer)


if __name__ == '__main__':
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    )
   
    conversation = """Given the context:
    Human: What is the actor library for scala?
    Bot: Akka.

    Answer the following question: What search term should the user type into google to find the documentation for what is in the bot's answer?
    """
    res = get_gpt_2_response(conversation)
    logger.info(res)