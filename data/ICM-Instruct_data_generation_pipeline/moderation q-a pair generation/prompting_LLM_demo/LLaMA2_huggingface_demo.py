# -*- coding: utf-8 -*-
import os
import json
from typing import List, Optional
from transformers import AutoTokenizer
import transformers
import torch
import time

if __name__ == '__main__':
    
    model = "/home/zyz/pretrained_models/llama-2-70b-chat-hf"

    tokenizer = AutoTokenizer.from_pretrained(model)
    pipeline = transformers.pipeline(
        "text-generation",
        model=model,
        torch_dtype=torch.float16,
        device_map="auto",
    )

    sequences = pipeline(
        'I liked "Breaking Bad" and "Band of Brothers". Do you have any recommendations of other shows I might like?\n',
        do_sample=True,
        top_k=10,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id,
        max_length=1024,
    )

    out = ''
    for seq in sequences:
        out += seq['generated_text']
    print(out)
    