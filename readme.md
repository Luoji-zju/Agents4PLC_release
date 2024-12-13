# Agents4PLC
A Multi-Agent System for Programmable Logic Controller (PLC) Code Generation based on IEC-61131 standard. The paper see:
[Agents4PLC: Automating Closed-loop PLC Code Generation and Verification in Industrial Control Systems using LLM-based Agents](https://arxiv.org/abs/2410.14209).

![Overview of our workflow.](pics/workflow.png)

## Dataset

The dataset is composed of benchmark dataset and RAG dataset, where released benchmarks are collected 
from open-source Github programs and we manually convert instruction into formalized and plcverif 
compatiable properties.

RAG dataset includes ST examples and tags are collected from [OSCAT dataset](http://www.oscat.de).

Industrial control documents and unreleased part of benchmark are collected from our partner companies
which are not prepared to be released.


## Source Code Organization

benchmark/ show the constructed tasks for plc code generation & verification task with patterns compatiable for plcverif verification.

result/ demonstrate the experiment statistics and detailed responses.

prompts/ contain specified prompts for each agent, including agent prompt engineering ways mentioned in our paper to 
enhance ability of agents.

LangChain/, MetaGPT/, LLM4PLC_reproduce/ or other folders corresponding to a certain multi agent framework's contain the implementation of the framework. You are free to create one for your own task, as long as the output satisfy the verification standards.

Notice: you should adjust content in config otherwise our framework could not work!

## Documents

For tools related to st compilation and smv verification not provided in src, see src/README.md.
For benchmark's construction process and how to use it, see benchmark/readme.md.

## Recommended Agent Related Tools & Works

Despite that our detailed code cannot be released due to cooperation with company, the following propose some recommended types 
to adjust multi-agent system, enhance ability of certain agents and reproduce experiments in out paper:  

| Agent       | Link |
| :--- | ----------- |
| MetaGPT     | https://github.com/geekan/MetaGPT                |
| LangGraph   | https://github.com/langchain-ai/langgraph        |
| ChatDev     | https://github.com/OpenBMB/ChatDev               |
| MapCoder    | [MapCoder: Multi-Agent Code Generation for Competitive Problem Solving](https://arxiv.org/abs/2405.11403) |




