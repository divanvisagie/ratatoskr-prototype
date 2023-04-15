import torch

from transformers import pipeline

try:
    torch.hub.load('huggingface/pytorch-transformers', 'model', 'databricks/dolly-v2-3b')
except Exception as e:
   print(e)
# generate_text = pipeline(model="databricks/dolly-v2-3b", trust_remote_code=True, device_map="auto")
