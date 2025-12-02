#!/bin/bash
log_dir=/home/lzh/Documents/LLM4PLC/LLM_4_PLC-reproduce/logs
text_gen_dir=/home/lzh/work/text-generation-webui
# conda activate /home/lzh/work/text-generation-webui/installer_files/env
cd $text_gen_dir

export CUDA_VISIBLE_DEVICES=0

# python server.py --api --listen --api-port 59945
python server.py --api --listen --api-port 59945 --loader llama.cpp\
                    --model codellama-34b-instruct.Q4_K_M.gguf \
                    --model-dir $text_gen_dir/models            
                    

# CMAKE_ARGS="-DLLAMA_CUDA=on" pip install llama-cpp-python --no-cache-dir