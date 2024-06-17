# Post-process MLLM output for LLM

## 1 Usage

### 1.1 Re-arrange

run **post_process_MLLM_output_4LLM_all_categories.py**:

```bash
python post_process_MLLM_output_4LLM_all_categories.py --base_folder_path ./CoT_prompts_1/all_LLaVA_results --save_folder_path ./CoT_prompts_1/all_LLaVA_results_revised
python post_process_MLLM_output_4LLM_all_categories.py --base_folder_path ./CoT_prompts_2/all_LLaVA_results --save_folder_path ./CoT_prompts_2/all_LLaVA_results_revised (optional)
python post_process_MLLM_output_4LLM_all_categories.py --base_folder_path ./CoT_prompts_3/all_LLaVA_results --save_folder_path ./CoT_prompts_3/all_LLaVA_results_revised (optional)
python post_process_MLLM_output_4LLM_all_categories.py --base_folder_path ./CoT_prompts_4/all_LLaVA_results --save_folder_path ./CoT_prompts_4/all_LLaVA_results_revised (optional)
python post_process_MLLM_output_4LLM_all_categories.py --base_folder_path ./CoT_prompts_5/all_LLaVA_results --save_folder_path ./CoT_prompts_5/all_LLaVA_results_revised (optional)
```

### 1.2 Delete wrong representations

run **check_all_MLLM_output_content.py**:

```bash
python check_all_MLLM_output_content.py --base_folder_path ./CoT_prompts_1/all_LLaVA_results --save_folder_path ./CoT_prompts_1/all_LLaVA_results_revised
python check_all_MLLM_output_content.py --base_folder_path ./CoT_prompts_2/all_LLaVA_results --save_folder_path ./CoT_prompts_2/all_LLaVA_results_revised (optional)
python check_all_MLLM_output_content.py --base_folder_path ./CoT_prompts_3/all_LLaVA_results --save_folder_path ./CoT_prompts_3/all_LLaVA_results_revised (optional)
python check_all_MLLM_output_content.py --base_folder_path ./CoT_prompts_4/all_LLaVA_results --save_folder_path ./CoT_prompts_4/all_LLaVA_results_revised (optional)
python check_all_MLLM_output_content.py --base_folder_path ./CoT_prompts_5/all_LLaVA_results --save_folder_path ./CoT_prompts_5/all_LLaVA_results_revised (optional)
```

### 1.3 Conclude the data

run **check_all_MLLM_output_num.py** (optional)
