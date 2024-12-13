# Original README
## LLM4PLC: Harnessing Large Language Models for Verifiable Model-Based Design in Industrial Control Systems
### Please refer to the project [website](https://sites.google.com/uci.edu/llm4plc/home) for the complete description and result showcase.

This research project aims to develop a novel approach to Model-Based Design (MBD) for Industrial Control Systems (ICS) by leveraging iterative prompting of Large Language Models (LLMs) to generate code for Programmable Logic Controllers (PLCs).
This repository contains published code, prompts, and descriptions of the LLM4PLC project.

## Architecture
To provide a high-level overview of the architecture of the LLM4PLC project, the following diagram is provided.

![figure](ims/im1.png "Architecture Diagram")

## Pre-Trained LoRAs
The pretrained loras are available [here](https://drive.google.com/file/d/1Z1XMpz9DJwcyJtPNyKRv8gVWspU0-DTo/view?usp=sharing). 
/largespace/workgroup/zrn/lora_checkpoints/llm4plc_loras
To use these, please refer to the instructions in [text-generation-webui](https://github.com/oobabooga/text-generation-webui).

##
Contributors:
Mohamad Fakih - mhfakih@uci.edu

Rahul Dharmaji - rdharmaj@uci.edu

Yasamin Moghaddas - ymoghadd@uci.edu


## Setting for reproduction:
Add a run.py in the main folder to simulate the workflow in LLM_4_PLC_repo/ims/im1.png.



## 现在服务器上有：
/largespace/llms/CodeLlama-7b-Instruct-hf
/largespace/workgroup/zrn/llm_checkpoints/codellama_13b/
/largespace/workgroup/zrn/llm_checkpoints/codellama_34b/

## 如何需要动态连接llm：
ln -s /largespace/llms/CodeLlama-7b-Instruct-hf /home/lzh/work/text-generation-webui/models/CodeLlama-7b-Instruct-hf
ln -s /largespace/workgroup/zrn/llm_checkpoints/codellama_13b/ /home/lzh/work/text-generation-webui/models/codellama_13b
ln -s /largespace/workgroup/zrn/llm_checkpoints/codellama_34b/ /home/lzh/work/text-generation-webui/models/codellama_34

how to run:
ln -s /home/lzh/work/src/matiec /home/lzh/work/LLM_4_PLC/matiec



