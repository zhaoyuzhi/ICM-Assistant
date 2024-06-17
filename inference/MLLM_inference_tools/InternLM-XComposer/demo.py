# -*- coding: utf-8 -*-
import torch
from transformers import AutoModel, AutoTokenizer

torch.set_grad_enabled(False)

# init model and tokenizer
model = AutoModel.from_pretrained('internlm/internlm-xcomposer-7b', trust_remote_code=True).cuda().eval()
tokenizer = AutoTokenizer.from_pretrained('internlm/internlm-xcomposer-7b', trust_remote_code=True)
model.tokenizer = tokenizer

# example image
image = 'examples/images/aiyinsitan.jpg'

# Single-Turn Pure-Text Dialogue
text = 'Please introduce Einstein.'
response = model.generate(text)
print(response)
# Albert Einstein was a German-born theoretical physicist who developed the general theory of relativity, one of the 
# two pillars of modern physics (alongside quantum mechanics). He is best known for his mass–energy equivalence 
# formula E = mc2 (which has been dubbed "the world's most famous equation"), and his explanation of the photoelectric 
# effect, both of which are examples of his special and general theories of relativity. Einstein is widely regarded as 
# one of the most influential physicists of all time.


# Single-Turn Text-Image Dialogue
text = 'Please introduce the person in this picture in detail.'
image = 'examples/images/aiyinsitan.jpg'
response = model.generate(text, image)
print(response)
# The person in the picture is Albert Einstein, a renowned theoretical physicist and one of the most influential 
# scientists of the 20th century. He is depicted in a black and white portrait, wearing a suit and tie, and has a 
# serious expression on his face.


# Multi-Turn Text-Image Dialogue
# 1st turn
text = 'Who is in the picture?'
response, history = model.chat(text=text, image=image, history=None)
print(response)
# Albert Einstein is in the picture.

# 2nd turn
text = 'What are his achievements?'
response, history = model.chat(text=text, image=None, history=history)
print(response)
# Albert Einstein was a German-born theoretical physicist who developed the general theory of relativity, 
# one of the two pillars of modern physics (alongside quantum mechanics). He is best known for his mass–energy 
# equivalence formula E = mc2 (which has been dubbed "the world's most famous equation"), and his explanation of 
# the photoelectric effect, both of which are examples of his special and general theories of relativity.

# 3rd turn
text = 'Is he the greatest physicist?'
response, history = model.chat(text=text, image=None, history=history)
print(response)
# Yes, Albert Einstein is widely regarded as one of the greatest physicists of all time.
