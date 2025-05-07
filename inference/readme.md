# Image Inference Scripts Collection

This project contains two distinct scripts to process images and perform inferences through large language models. Choose the appropriate method based on your requirements.

## Method 1: Using `lmdeploy` with Softmax Calculation (`vllm_inference/vllm_inference_logits.py`)

### Features
- Specifically designed for evaluating whether an image is "sexy".
- Calculates a softmax score based on logits output by the model to determine if the image meets the specified criteria.

### How to Run
1. Ensure you have the necessary dependencies installed:
   ```bash
   pip install lmdeploy transformers
   ```
2. Modify the script to match your environment's model name and other configurations.
3. Prepare a text file containing absolute paths to your images.
4. Execute the script:
   ```bash
   python vllm_inference_logits.py
   ```
5. Review the generated JSON file to get analysis results for each image.

### Sample Output Format (JSON)
```json
[
    {
        "image_name": "not-sexy_00007639.jpg",
        "logit_yes": 13.9296875,
        "logit_no": 17.859375,
        "sexy_score": 0.019271137919768803,
        "sexy_conclusion": "No"
    },
    ...
]
```

## Method 2: Using `requests` Library to Interact with External Model Service (`vllm_inference/vllm_inference.py`)

### Features
- More flexible and suitable for any type of image description or classification tasks.
- Interacts with a remotely deployed language model service via HTTP requests.

### How to Run
1. Install the required Python packages:
   ```bash
   pip install requests
   ```
2. Adjust the script according to your actual deployment, such as the API endpoint of your model server.
3. Create a text file containing paths to the images you want to process.
4. Run the script:
   ```bash
   python vllm_inference.py
   ```
5. The output will be saved in a TXT file, making it easy to review and analyze further.

### Sample Output Format (TXT)
```
/path/to/not-sexy_00007639.jpg
Explain why this image is sexy or not ...
Explain ...
/path/to/sexy_00001234.jpg
Explain why this image is sexy or not ...
Explain ...
...
```