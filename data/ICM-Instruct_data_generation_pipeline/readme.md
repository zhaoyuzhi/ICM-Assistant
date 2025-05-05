# Data Labeling

## 1 Rule Definition and Image Collection

- Define some moderation terms

- Convert moderation terms into attribute combination

- Write explicit description

## 2 Moderation Explanation Generation

### 2.1 prompting MLLM

- use **MLLM_inference_bylist**

### 2.2 Convert MLLM's output to LLM's input

- use **post_process_MLLM_output_for_LLM**

## 3 Moderation Q-A Pair Generation

- use **prompting_LLM**

- or use **prompting_LLM_client**
