## create a basic llm calling model, without the absence of langchain or any workflow in single agent.
## used for reproducing LLM4PLC.

from openai import OpenAI
import sys
from pathlib import Path
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))

from config import chat_model, openai_api_key, openai_base_url

def call_llm(sys_msg, user_msg):
    # if chat_model == "deepseek_api":
    #     model = "deepseek-chat"
    #     openai_api_key = "sk-a8ab3774a0eb44929c873515b61fc4b4"
    #     openai_api_base = "https://api.deepseek.com/v1"
    # elif chat_model == "codellama_localhost_gen":
    #     model = "codellama-34b-instruction-hf"
    #     openai_api_key = "EMPTY"
    #     openai_api_base = "http://localhost:8000/v1"
    # elif chat_model == "codellama_localhost_fix":
    #     model = "codellama-34b-instruction-hf"
    #     openai_api_key = "EMPTY"
    #     openai_api_base = "http://localhost:8001/v1"

    client = OpenAI(
        api_key=openai_api_key,
        base_url=openai_base_url,
    )

    print(f"Calling LLM with system message: {sys_msg}")
    print(f"User message: {user_msg}")

    completion = client.chat.completions.create(
        model=chat_model,
        messages=[
            {"role": "system", "content": sys_msg},
            {"role": "user", "content": user_msg}
        ]
    )

    response_content = completion.choices[0].message.content
    print(f"LLM response content: {response_content}")
    
    return response_content