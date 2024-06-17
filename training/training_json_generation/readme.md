# Create json for MLLM training

## 1 Guidance

Please run the **run.py** file to obtain training json data for MLLMs.

```bash
python run.py
```

Parameters:

- model-type: related to the json format, defined by the model type
- llava_v1_5_mix665k.json
- pathto/qa/open_qa/
- pathto/qa/reasoning/

## 2 Notes

- Change file path
- Run step 1, saving stage 1 json.
- Run step 2 with stage 1 json, saving stage 2 json 
- Modify finetune.sh dataset path to stage 2 json
