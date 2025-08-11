# GLM-4.1V-Thinking

[中文阅读](./README_zh.md)

<div align="center">
<img src=resources/logo.svg width="40%"/>
</div>
<p align="center">
    👋 Join our <a href="resources/WECHAT.md" target="_blank">Wechat</a> or <a href="https://discord.com/invite/8cnQKdAprg" target="_blank">Discord</a>
    <br>
    📖 View the GLM-4.1V-9B-Thinking <a href="https://arxiv.org/abs/2507.01006" target="_blank">paper</a>.
    <br>
    💡 Try the <a href="https://huggingface.co/spaces/THUDM/GLM-4.1V-9B-Thinking-API-Demo" target="_blank">Hugging Face</a> or <a href="https://modelscope.cn/studios/ZhipuAI/GLM-4.1V-9B-Thinking-Demo" target="_blank">ModelScope</a> online demo for GLM-4.1V-9B-Thinking.
    <br>
    📍 Using GLM-4.1V-9B-Thinking API at <a href="https://www.bigmodel.cn/dev/api/visual-reasoning-model/GLM-4.1V-Thinking">Zhipu Foundation Model Open Platform</a>
</p>

## Project Updates

- 🔥 **News**: `2025/07/16`: We have open-sourced the **VLM Reward System** used in training GLM-4.1V-Thinking! Check out the [repo here](https://github.com/THUDM/GLM-4.1V-Thinking/tree/main/glmv_reward) and try it locally: `python examples/reward_system_demo.py`

- **News**: `2025/07/02`: The [GLM-4.1V-9B-Thinking series](https://huggingface.co/THUDM/GLM-4.1V-9B-Thinking) is now open-sourced! Supports enhanced visual reasoning and agent interaction.

- **News**: `2025/07/01`: We released the [Technical Report](https://arxiv.org/abs/2507.01006) for GLM-4.1V-Thinking.

## Model Introduction

Vision-Language Models (VLMs) have become foundational components of intelligent systems. As real-world AI tasks grow
increasingly complex, VLMs must evolve beyond basic multimodal perception to enhance their reasoning capabilities in
complex tasks. This involves improving accuracy, comprehensiveness, and intelligence, enabling applications such as
complex problem solving, long-context understanding, and multimodal agents.

Based on the [GLM-4-9B-0414](https://github.com/THUDM/GLM-4) foundation model, we present the new open-source VLM model
**GLM-4.1V-9B-Thinking**, designed to explore the upper limits of reasoning in vision-language models. By introducing
a "thinking paradigm" and leveraging reinforcement learning, the model significantly enhances its capabilities. It
achieves state-of-the-art performance among 10B-parameter VLMs, matching or even surpassing the 72B-parameter
Qwen-2.5-VL-72B on 18 benchmark tasks. We are also open-sourcing the base model GLM-4.1V-9B-Base to
support further research into the boundaries of VLM capabilities.

![rl](resources/rl.jpeg)

Compared to the previous generation models CogVLM2 and the GLM-4V series, **GLM-4.1V-Thinking** offers the
following improvements:

1. The first reasoning-focused model in the series, achieving world-leading performance not only in mathematics but also
   across various sub-domains.
2. Supports **64k** context length.
3. Handles **arbitrary aspect ratios** and up to **4K** image resolution.
4. Provides an open-source version supporting both **Chinese and English bilingual** usage.

## Model Information

### Model Download Links

| Model                | Download Links                                                                                                                                      | Model Type      |
|----------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|-----------------|
| GLM-4.1V-9B-Thinking | [🤗 Hugging Face](https://huggingface.co/THUDM/GLM-4.1V-9B-Thinking)<br> [🤖 ModelScope](https://modelscope.cn/models/ZhipuAI/GLM-4.1V-9B-Thinking) | Reasoning Model |
| GLM-4.1V-9B-Base     | [🤗 Hugging Face](https://huggingface.co/THUDM/GLM-4.1V-9B-Base)<br> [🤖 ModelScope](https://modelscope.cn/models/ZhipuAI/GLM-4.1V-9B-Base)         | Base Model      |

The model's algorithm implementation can be found in the
official [transformers](https://github.com/huggingface/transformers/tree/main/src/transformers/models/glm4v) repository.

### Runtime Requirements

#### Inference

| Device (Single GPU) | Framework    | Min Memory | Speed              | Precision |
|---------------------|--------------|------------|--------------------|-----------|
| NVIDIA A100         | transformers | 22GB       | 14 - 22 Tokens / s | BF16      |
| NVIDIA A100         | vLLM         | 22GB       | 60 - 70 Tokens / s | BF16      |

#### Fine-tuning

The following results are based on image fine-tuning using the [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory)
toolkit.

| Device (Cluster) | Strategy   | Min Memory / # of GPUs | Batch Size (per GPU) | Freezing    |
|------------------|------------|------------------------|----------------------|-------------|
| NVIDIA A100      | LORA       | 21GB / 1 GPU           | 1                    | Freeze VIT  |
| NVIDIA A100      | FULL ZERO2 | 280GB / 4 GPUs         | 1                    | Freeze VIT  |
| NVIDIA A100      | FULL ZERO3 | 192GB / 4 GPUs         | 1                    | Freeze VIT  |
| NVIDIA A100      | FULL ZERO2 | 304GB / 4 GPUs         | 1                    | No Freezing |
| NVIDIA A100      | FULL ZERO3 | 210GB / 4 GPUs         | 1                    | No Freezing |

> Note: Fine-tuning with Zero2 may result in zero loss; Zero3 is recommended for stable training.

## Benchmark Performance

Based on the [GLM-4-9B-0414](https://github.com/THUDM/GLM-4) foundation model, we present the new open-source VLM model
**GLM-4.1V-9B-Thinking**, which introduces a "thinking" paradigm and leverages Reinforcement Learning with Curriculum
Sampling (RLCS) to comprehensively enhance model capabilities.
It achieves state-of-the-art performance among vision-language models at the 10B parameter scale, matching or even
surpassing the 72B Qwen-2.5-VL on 18 benchmark tasks.
We also open-source the base model **GLM-4.1V-9B-Base** to support further research on the frontier of vision-language
models.

![bench](resources/bench.jpeg)

## Model Inference

All inference scripts are located in the `inference` folder and include:

- `trans_infer_cli.py`: A command-line interactive script using the `transformers` library as the backend. It supports
  multi-turn dialogue.
- `trans_infer_gradio.py`: A Gradio-based web UI script using the `transformers` backend. It supports multimodal inputs
  such as images, videos, PDFs, and PPTs.
- OpenAI-compatible API service with `vllm`, along with a simple request example provided in `vllm_api_request.py`.

    ```shell
    vllm serve THUDM/GLM-4.1V-9B-Thinking --limit-mm-per-prompt '{"image":32}' --allowed-local-media-path /
    ```

  - If `--limit-mm-per-prompt` is not specified, only 1 image is supported. The model supports a maximum of 1 video or
    300 images per input — it does **not** support simultaneous image and video inputs.
  - `--allowed-local-media-path` must be set to permit access to local multimodal inputs.

- `trans_infer_bench`: Academic benchmarking script for inference with `GLM-4.1V-9B-Thinking`. Key features:
  - Automatically interrupts thinking if it exceeds 8192 tokens and appends `</think><answer>` to prompt the model to
    generate a final answer.
  - Demonstrates video-based input; for other modalities, modifications are required.
  - Only a `transformers` version is provided. For `vLLM`, a custom implementation is needed to support this logic.

- `vllm_request_gui_agent.py`: This script demonstrates how to handle model responses and construct prompts for GUI
  Agent use cases. It covers strategies for mobile, desktop, and web environments, and can be integrated into your
  application framework. For detailed documentation about GUI Agent, please refer to [this file](resources/agent.md).

- For Ascend NPU Inference, Check [here](https://gitee.com/ascend/MindSpeed-MM/tree/master/examples/glm4.1v/README.md).

## Model Fine-tuning

[LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory) now supports fine-tuning of this model. Below is an example
dataset using two images. Prepare your dataset in a `finetune.json` file like the following:

```json
[
  {
    "messages": [
      {
        "content": "<image>Who are they?",
        "role": "user"
      },
      {
        "content": "<think>\nUser ask me to observe the image and get the answer. I Know they are Kane and Gretzka from Bayern Munich.</think>\n<answer>They're Kane and Gretzka from Bayern Munich.</answer>",
        "role": "assistant"
      },
      {
        "content": "<image>What are they doing?",
        "role": "user"
      },
      {
        "content": "<think>\nI need to observe what this people are doing. Oh, They are celebrating on the soccer field.</think>\n<answer>They are celebrating on the soccer field.</answer>",
        "role": "assistant"
      }
    ],
    "images": [
      "mllm_demo_data/1.jpg",
      "mllm_demo_data/2.jpg"
    ]
  }
]
```

1. Content inside `<think> ... </think>` will **not** be stored in the conversation history or used during fine-tuning.
2. The `<image>` tag will be replaced with actual image data during preprocessing.

After preparing the dataset, you can proceed with fine-tuning using the standard LLaMA-Factory pipeline.

## Model License

- The code in this repository is released under the [Apache License 2.0](LICENSE).
- The models **GLM-4.1V-9B-Thinking** and **GLM-4.1V-9B-Base** are both licensed under the **MIT License**.

## Citation

If you find our work helpful, please consider citing the following paper.

```bibtex
@misc{glmvteam2025glm41vthinkingversatilemultimodalreasoning,
      title={GLM-4.1V-Thinking: Towards Versatile Multimodal Reasoning with Scalable Reinforcement Learning}, 
      author={GLM-V Team and Wenyi Hong and Wenmeng Yu and Xiaotao Gu and Guo Wang and Guobing Gan and Haomiao Tang and Jiale Cheng and Ji Qi and Junhui Ji and Lihang Pan and Shuaiqi Duan and Weihan Wang and Yan Wang and Yean Cheng and Zehai He and Zhe Su and Zhen Yang and Ziyang Pan and Aohan Zeng and Baoxu Wang and Boyan Shi and Changyu Pang and Chenhui Zhang and Da Yin and Fan Yang and Guoqing Chen and Jiazheng Xu and Jiali Chen and Jing Chen and Jinhao Chen and Jinghao Lin and Jinjiang Wang and Junjie Chen and Leqi Lei and Letian Gong and Leyi Pan and Mingzhi Zhang and Qinkai Zheng and Sheng Yang and Shi Zhong and Shiyu Huang and Shuyuan Zhao and Siyan Xue and Shangqin Tu and Shengbiao Meng and Tianshu Zhang and Tianwei Luo and Tianxiang Hao and Wenkai Li and Wei Jia and Xin Lyu and Xuancheng Huang and Yanling Wang and Yadong Xue and Yanfeng Wang and Yifan An and Yifan Du and Yiming Shi and Yiheng Huang and Yilin Niu and Yuan Wang and Yuanchang Yue and Yuchen Li and Yutao Zhang and Yuxuan Zhang and Zhanxiao Du and Zhenyu Hou and Zhao Xue and Zhengxiao Du and Zihan Wang and Peng Zhang and Debing Liu and Bin Xu and Juanzi Li and Minlie Huang and Yuxiao Dong and Jie Tang},
      year={2025},
      eprint={2507.01006},
      archivePrefix={arXiv},
      primaryClass={cs.CV},
      url={https://arxiv.org/abs/2507.01006}, 
}
```
