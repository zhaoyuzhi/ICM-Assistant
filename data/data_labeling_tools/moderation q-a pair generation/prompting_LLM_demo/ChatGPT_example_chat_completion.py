import os
import json
import pdb
import random
import openai
import time
from datetime import datetime
from time import sleep
from tqdm import tqdm

def llm_client(api_key, llm_model, user_content):
    request_start = time.time()
    # load api key
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model=llm_model,
        messages=[
            {"role": "user",
             "content": user_content},
        ],
        temperature=0.2,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    request_duration = time.time() - request_start
    print(f"Successful LLM query. It took {request_duration:.2f}s")
    return response.choices[0]["message"]["content"]

if __name__ == "__main__":

    api_key = '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'
    user_content = 'who are you?'
    text = llm_client(api_key, 'gpt-4-1106-preview', user_content)
    print(text)
