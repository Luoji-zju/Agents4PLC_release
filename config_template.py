### !!! warning !!! ###
# Refer to this format of config and write your own api-key in config.py. This canbe imported by your multi agent frameworks.

### must be configged area ###
# model config: refer to src/langchain_create_agent to define it
# chat_model = "openai"
# embedding_model = "text-embedding-ada-002"
    
# config for general url & key are remained (to avoid potential errors) 
# you can use model to decide tool-specified url & key:
# (deepseek_base_url, deepseek_api_key & openai_base_url, openai_api_key)
# which correspond to used models in our framework
# base_url = "https://api.openai.com/v1"
# api_key = "sk-your-own-key-here"

# MATIEC_PATH = "/home/work/src/matiec" 

### alternative ###
# threshold for plcverif evaluation pass rate.
# plcverif_verified_threshold = 0.80
# plcverif_passed_threshold = 0.80

# compiler used in evaluation process, by default "rusty" if not selected. alternative for "matiec".
# evaluate_compiler = "rusty"

# max_tokens, which could satisfy the need of  input size for certain model that limits context window
# max_tokens = 4500

# terminated since folder path is now directly transfered to langGraph workflow kwargs.
# folder_path = "/home/work/result/generation_log_20240703142338339087"



