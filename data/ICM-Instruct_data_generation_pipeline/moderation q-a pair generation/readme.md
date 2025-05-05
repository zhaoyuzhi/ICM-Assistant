# Prepare LLM output for further training (Generating Yes/No, What/How, Multi-Choise data)

## 1 Usage

run **prompting_LLaMA2_client.py**:
Please choose your own deployed LLM API for generating Yes/No, What/How, Multi-Choise data of the input explainations of sexy images. Please contact the authors for the original ICM-Sexy images for training.


### 1.1 Prompt LLM for Yes/No and What/How data

```bash
python script_name.py --txt_path "your/path/to/txt" --q_type "qa" --vllm_address "http://your_custom_vllm_address"
```

### 1.2 Prompt LLM for Multi-Choise data

```bash
python script_name.py --txt_path "your/path/to/txt" --q_type "mc" --vllm_address "http://your_custom_vllm_address"
```

### 1.3 Prompt LLM for mixed data at once

```bash
python script_name.py --txt_path "your/path/to/txt" --q_type "mixed" --vllm_address "http://your_custom_vllm_address"
```