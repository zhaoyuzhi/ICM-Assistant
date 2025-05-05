# -*- coding: utf-8 -*-
import os
from transformers import AutoTokenizer
import transformers
import torch

if __name__ == '__main__':

    model = "/home/zyz/pretrained_models/llama-2-70b-chat-hf"
    model = "D:\\pretrained_models\\LLaVa\\full\\llava-v1.5-13b"
    model = "D:\\pretrained_models\\Llama-2-70b-chat-hf"

    # 要自动下载在特定模型在预训练或微调期间使用的vocab，可以使用from_pretrained()方法
    tokenizer = AutoTokenizer.from_pretrained(model)

    print('-------------------------------------------------------------------------')
    sequence = "Using a Transformer network is simple"
    print(sequence)

    print('-------------------------------------------------------------------------')
    # PreTrainedTokenizer有很多方法，但是你需要记住的唯一方法是它的__call__
    # 只需要将文本序列提供给tokenizer对象即可
    # 返回的是一个字典，里面的列表包含了int类别的数据。其中：
    # input_id是对应于文本序列中每个token的索引（在vocab中的索引）
    # attention_mask是对应于注意力机制的计算，各元素的值为0或1，如果当前token被mask或者是只是用来作为填充的元素，那么其不需要进行注意力机制的计算，其值为0
    # token_type_ids是对应于不同的文本序列，例如在NSP（BERT及某些语言模型中的“Next Sentence Prediction”）任务中需要输入两个文本序列
    encoded_input = tokenizer(sequence)
    print(encoded_input)
    print(encoded_input.tokens()) 
    print(encoded_input.word_ids())
    print(encoded_input["input_ids"])

    print('-------------------------------------------------------------------------')
    # 输入的是索引，tokenizer可以进行反向解码
    decoded_input = tokenizer.decode(encoded_input["input_ids"])
    print(decoded_input)
    decoded_input = tokenizer.decode(encoded_input["input_ids"][1:])
    print(decoded_input)

    print('-------------------------------------------------------------------------')
    # tokenizer的具体方法
    tokens = tokenizer.tokenize(sequence)
    print(tokens)
    if tokenizer.pad_token is None:
        tokenizer.add_special_tokens({'pad_token': '[PAD]'})
    encoded_tokens = tokenizer.encode(sequence, max_length=32, pad_to_max_length=True)
    print(encoded_tokens)
    print('-------------------------------------------------------------------------')
