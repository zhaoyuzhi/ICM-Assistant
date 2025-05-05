# Prepare MLLM output for LLM (Generating explaination data)

## 1 Usage

### 1.1 Prompt MLLM for explaniantion data

run **vllm_data_generation.py**:
Please choose your own deployed MLLM API for generating explainations of the input sexy images. Please contact the authors for the original ICM-Sexy images for training.

```bash
python vllm_data_generation.py --vlm_address "http://your_custom_address" --input_dir "path/to/your/input/images" --output_dir "path/to/your/output/texts"
```

### 1.2 Re-arrange

run **post_process_MLLM_output_4LLM_all_categories.py**:

```bash
python post_process_MLLM_output_4LLM_all_categories.py --base_folder_path path/to/your/output/texts --save_folder_path path/to/your/output/text_revised
```

### 1.3 Delete wrong representations

run **check_all_MLLM_output_content.py**:

```bash
python check_all_MLLM_output_content.py --base_folder_path path/to/your/output/texts --save_folder_path path/to/your/output/text_revised
```

### 1.4 Conclude the data

run **check_all_MLLM_output_num.py** (optional)