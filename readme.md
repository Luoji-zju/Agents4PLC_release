# Agents4PLC
A Multi-Agent System for Programmable Logic Controller (PLC) Code Generation based on IEC-61131 standard. The paper see:
[Agents4PLC: Automating Closed-loop PLC Code Generation and Verification in Industrial Control Systems using LLM-based Agents](https://arxiv.org/abs/2410.14209).

![Overview of our workflow.](pics/workflow.png)

## Dataset

**Dataset v2.0 – New Extended Release**

The dataset accompanies a new extension of Agents4PLC with a newly extended **benchmark dataset** of 70 *medium* cases and 3 *hard* cases. If you need functionality code to execute the formal specs, see [https://github.com/Luoji-zju/Agents4PLC_release]

### Purpose & Role of the Dataset

In Agents4PLC we established the **first verifiable benchmark** for automatically generating IEC-61131-3 Structured-Text (ST) code from natural-language requirements. The dataset serves three goals:

1. Provide **formal specifications** (nuXmv / PLCverif compatible) so that correctness can be proven automatically.
2. Supply **human-checked reference ST code** that compiles and satisfies the specs.
3. Enable **fair comparison** of more complex PLC-code generation tasks with advanced tasks.

### What's New in Dataset v2.0

| Item | v1.0 (arXiv) | v2.0 (this release) |
|---|---|---|
| **#tasks** | 23 | **96** (23 + 73) |
| **Task IDs** | not identified | M1-M70, H1-H3 |
| **Granularity** | easy / medium | medium / **hard** |
| **Quality gates** | basic manual review | manual review with PLC engineers **+** fine-tuned LLM evaluator |
| **Annotations** | spec + reference | + difficulty tag |

All 73 new tasks are **tagged with new prefix** to avoid collisions with v1.0.

### File Layout

```
benchmark_v1/
│   ├── easy.jsonl
│   └── medium.jsonl
benchmark_v2/
│   ├── medium.jsonl
│   └── hard.jsonl
├── readme.md
```

The dataset is composed of benchmark dataset and RAG dataset, where released benchmarks are collected from open-source Github programs and we manually convert instruction into formalized and plcverif compatiable properties.

## Source Code Organization

benchmark_v1/ and benchmark_v2/ show the constructed tasks for plc code generation & verification task with patterns compatiable for plcverif verification.

result/ demonstrate the experiment statistics and detailed responses.

prompts/ contain specified prompts for each agent, including agent prompt engineering ways mentioned in our paper to 
enhance ability of agents.

LangChain/, MetaGPT/, LLM4PLC_reproduce/ or other folders corresponding to a certain multi agent framework's contain the implementation of the framework. You are free to create one for your own task, as long as the output satisfy the verification standards. (not available)

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

### Citation

If you want to use this dataset, please cite:

```
@article{liu2024agents4plc,
  title={Agents4plc: Automating closed-loop plc code generation and verification in industrial control systems using llm-based agents},
  author={Liu, Zihan and Zeng, Ruinan and Wang, Dongxia and Peng, Gengyun and Wang, Jingyi and Liu, Qiang and Liu, Peiyu and Wang, Wenhai},
  journal={arXiv preprint arXiv:2410.14209},
  year={2024}
}
```




