
    
<h1>ICM-Assistant: Instruction-tuning Multimodal Large Language Models for Rule-based Explainable Image Content Moderation</h1>

<div> AAAI 2025 </div>

<div>
   <a href="https://huggingface.co/datasets/zhaoyuzhi/ICM-Instruct"><strong>Dataset</strong></a> | 
   <a href="https://huggingface.co/collections/zhaoyuzhi/icm-assistant-6790a2053c1b3f65df4e2541"><strong>Model Zoo</strong></a> |  
   <a href="https://arxiv.org/abs/2412.18216"><strong>Paper</strong></a>
   </div>   

    
  <div style="width: 100%; text-align: center; margin:auto;">
      <img style="width:100%" src="./fig/teaser.png">
  </div>
</div>   
  

## Quick Start


### LLaVA-v1.5

#### Install LLaVA.

```shell
git clone https://github.com/haotian-liu/LLaVA.git
cd LLaVA
pip install -e .
```

#### Simple Interactive Demos.

*See the codes and scripts below.*

<details>
<summary>Example Code (CLI Demo for Multi-turn Conversation)</summary>
    
```shell
python -m llava.serve.cli \
    --model-path zhaoyuzhi/ICM-LLaVA-v1.5-7B \
    --image-file "fig/sexy.jpg" \
```

Note: The results may contain randomness as `do_sample=True` is enabled during conversation mode. 

</details>


#### Quantitative Evaluations

<details>
<summary>ICM Acc. in ICM-Val.</summary>
    
```shell
python eval_scripts/llava_v1.5/eval_val.py
```
    
</details>


<details>
<summary>ICM Acc. in ICM-Test</summary>
    
```shell
python eval_scripts/llava_v1.5/eval_test.py
```

</details>


<details>
<summary>Moderation Q-A Acc. in ICM-Val</summary>
    
```shell
python eval_scripts/llava_v1.5/eval_MQA.py
```

</details>

<details>
<summary>Moderation Explanation Acc. in ICM-Val</summary>
    
```shell
python eval_scripts/llava_v1.5/eval_MEQ.py
```

</details>


### Other MLLMs are pending

<!-- *For mPLUG-Owl-2, Only Single GPU Inference is supported now. Please set environmental variable (e.g. `export CUDA_VISIBLE_DEVICES=0`) to make sure that the model can be loaded on only one device.* -->


## Training

- [Training Docs for LLaVA-v1.5/LLaVA-v1.6](scripts/llava_v1.5)
- [Training Docs for mPLUG-Owl-2](scripts/mplug_owl_2)
<!-- - [Training Docs for InternVL](scripts/llava_v1.5)
- [Training Docs for mPLUG-Owl-2](scripts/mplug_owl_2)
- [Training Docs for LLaVA-v1.5](scripts/llava_v1.5)
- [Training Docs for mPLUG-Owl-2](scripts/mplug_owl_2)
 -->
## License

Researchers and open-source developers are **free** to use the **ICM-Assistant** dataset and the fine-tuned weights as provided for the four MLLMs. We also allow commercial use, while any commercial use should be pre-permitted by our team. Please email `mywu@cse.cuhk.edu.hk` to gain the permission for commercial use.

## Citation

If you consider this work interesting, please feel free to cite it in your work!

```bibtex
@misc{wu2025icmassistantinstructiontuningmultimodallarge,
      title={ICM-Assistant: Instruction-tuning Multimodal Large Language Models for Rule-based Explainable Image Content Moderation}, 
      author={Mengyang Wu and Yuzhi Zhao and Jialun Cao and Mingjie Xu and Zhongming Jiang and Xuehui Wang and Qinbin Li and Guangneng Hu and Shengchao Qin and Chi-Wing Fu},
      year={2025},
      eprint={2412.18216},
      archivePrefix={arXiv},
      primaryClass={cs.CV},
      url={https://arxiv.org/abs/2412.18216}, 
}
```

