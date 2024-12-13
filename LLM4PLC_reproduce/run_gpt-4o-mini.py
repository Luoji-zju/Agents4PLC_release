############## a lot of content to modify!

from openai import OpenAI
import os
import time
import subprocess
import re
import os
import threading

from pathlib import Path
import sys
from datetime import datetime
import os

# Resolve the parent directory for whole program and llm4plc itself as an absolute path
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))

LLM4PLC_parent_dir = Path(__file__).resolve().parent
# sys.path.append(str(LLM4PLC_parent_dir))

from LangChain.test_multi_agent_framework import parse_plc_instructions


############# function tools #################
# 模拟 OpenAI API 调用的函数，增加打印输入和输出
def call_llm(sys_msg, user_msg, mode="gpt_4o_mini"):
    if mode == "deepseek_api":
        model = "deepseek-chat"
        openai_api_key = "sk-a8ab3774a0eb44929c873515b61fc4b4"
        openai_api_base = "https://api.deepseek.com/v1"
    elif mode == "codellama_localhost_gen":
        model = "codellama-34b-instruction-hf"
        openai_api_key = "EMPTY"
        openai_api_base = "http://localhost:8000/v1"
    elif mode == "codellama_localhost_fix":
        model = "codellama-34b-instruction-hf"
        openai_api_key = "EMPTY"
        openai_api_base = "http://localhost:8001/v1"
    elif mode == "gpt_4o":
        model = "gpt-4o"
        openai_api_key = "sk-SrBZmYxKfnyJyO4k23D282A0228642439432Fb0511B93627"
        openai_api_base = "https://xiaoai.plus/v1"
    elif mode == "gpt_4o_mini":
        model = "gpt-4o-mini"
        openai_api_key = "sk-SrBZmYxKfnyJyO4k23D282A0228642439432Fb0511B93627"
        openai_api_base = "https://xiaoai.plus/v1"

    client = OpenAI(
        api_key=openai_api_key,
        base_url=openai_api_base,
    )

    print(f"Calling LLM with system message: {sys_msg}")
    print(f"User message: {user_msg}")

    # 调用 LLM 并获取返回
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": sys_msg},
            {"role": "user", "content": user_msg}
        ]
    )

    # 提取消息内容
    response_content = completion.choices[0].message.content
    print(f"LLM response content: {response_content}")
    
    return response_content

def nuXmv_model_checker(smv_content, smv_file_path):
    """
    使用 nuXmv 进行模型检查，返回验证结果。
    """
    try:
        result = subprocess.run(['nuXmv', smv_file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except subprocess.CalledProcessError as e:
        max_len = 1000  # 限制最大错误信息长度
        err_info = e.stderr.decode()[:max_len] if len(e.stderr) > max_len else e.stderr.decode()
        return f'SMV code compilation failed.\n Origin SMV code: {smv_content}\n CodeError: {err_info}'

    # 解析输出
    output = result.stdout.decode()

    # 查找是否有违反规范的情况
    spec_fail_match = re.search(r'specification .+ is false', output)
    if spec_fail_match:
        index = spec_fail_match.end()
        end_index = output.find('\n', index)
        end_index = output.find('\n', end_index + 1)
        return f'SMV Validation failed: {output[index:end_index].strip()}'

    return 'SMV Validation successful'


def input_with_timeout(prompt, timeout=30, default=""):
    """
    Prompts the user for input with a timeout. Returns the default value if the user does not respond in time.

    Args:
        prompt (str): The prompt to display to the user.
        timeout (int): The time to wait for user input, in seconds. Default is 30 seconds.
        default (str): The default value to return if no input is given within the timeout period.

    Returns:
        str: The user's input or the default value if the timeout expires.
    """
    user_input = [default]

    def get_input():
        try:
            user_input[0] = input(prompt)
        except EOFError:
            user_input[0] = default

    input_thread = threading.Thread(target=get_input)
    input_thread.start()
    input_thread.join(timeout)

    # If thread is still alive after timeout, use default value
    if input_thread.is_alive():
        print(f"\nNo response received within {timeout} seconds. Using default value: '{default}'")
        return default

    return user_input[0]

def simple_log_message(message, log_file_path):
    """Logs a simple message to the log file with timestamp."""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    
    # Open the log file in append mode
    with open(log_file_path, 'a') as log_file:
        log_file.write("="*50 + "\n")  # Separator line
        log_file.write(f"Timestamp: {timestamp}\n")
        log_file.write(f"{message}\n")

def log_message(log_file_path, sys_msg, user_msg, result, phase_name="Unknown phase"):
    """Logs the system message, user message, and model response with timestamp to the log file."""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    
    # Open the log file in append mode
    with open(log_file_path, 'a') as log_file:  # 'a' mode means append
        log_file.write("="*50 + "\n")  # Separator line
        log_file.write(f"Phase: {phase_name}\n")
        log_file.write(f"Timestamp: {timestamp}\n")
        log_file.write(f"System Message:\n{sys_msg}\n")
        log_file.write(f"User Message:\n{user_msg}\n")
        log_file.write(f"Model Response:\n{result}\n")


def create_log_directory(spec_path, base_dir="/home/lzh/work/LLM_4_PLC/log"):
    """
    Creates a log directory with a file to store the interaction process.
    The default storage path is "{base_dir}/{timestamp}_{spec_name}".
    In case spec_path is "" or None, the spec_name is None and log_dir = f"{base_dir}/{timestamp}".
    """
    # Create the directory path with timestamp
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    
    # Handle the case where spec_path is None or empty
    if not spec_path:
        spec_name = None
        log_dir = f"{base_dir}/{timestamp}"
    else:
        spec_name = os.path.basename(spec_path).split('.')[0]
        log_dir = f"{base_dir}/{timestamp}_{spec_name}"
    
    # Ensure the log directory exists
    os.makedirs(log_dir, exist_ok=True)
    
    # Create the log.txt file path
    log_file_path = os.path.join(log_dir, "log.txt")
    return log_file_path, log_dir

def extract_section(text, start_tag, end_tag):
    """ Helper function to extract content between start and end tags, excluding the tags themselves.
        in case nothing extracted, return the whole content"""
    start_idx = text.find(start_tag)
    end_idx = text.find(end_tag)

    if start_idx == -1 or end_idx == -1:
        return text

    # 提取时，start_tag后开始，end_tag前结束
    # aaa = text[start_idx + len(start_tag):end_idx].strip()
    return text[start_idx + len(start_tag):end_idx].strip()


def extract_plan_and_question(text):
    """ 
        提取 plan 和 question 的改进方法:
        - 如果未识别到 question, 返回全部内容作为 plan。
        - 如果识别到 question 和 plan, 按相应顺序提取它们的内容。
    """
    plan = extract_section(text, "[START_PLAN]", "[END_PLAN]")
    question = extract_section(text, "[START_QUESTION]", "[END_QUESTION]")

    if not plan:
        plan = text

    return plan, question

### automatically turn json-format data into ltl & ctl sentences
def generate_smv_compatible_ltl_ctl_model(property_data):
    """
    Generates SMV-compatible LTL/CTL model based on the provided job request pattern and pattern ID.

    Args:
        property_data (dict): A dictionary containing the property details, including job_req and pattern_id.

    Returns:
        str: The generated SMV-compatible LTL/CTL model or an empty string if job_req is not 'pattern' or required fields are missing.
    """
    def convert_pattern_params(pattern_params):
        """
        Convert pattern_params from numeric keys to named keys and adjust the expression to match nuXmv syntax.

        Args:
            pattern_params (dict): Dictionary with numeric keys ("1", "2", "3").

        Returns:
            dict: Dictionary with named keys ("param1", "param2", "param3") and formatted expressions.
        """
        # 定义操作符替换库，支持所有语法中提到的操作符
        operator_replacements = {
            "AND": "&",
            "&&": "&",
            "∧": "&",
            "OR": "|",
            "∨": "|",
            "NOT": "!",
            "¬": "!",
            "-->": "->",       # 蕴含
            "→": "->",
            "⇒": "->",
            "<->": "<->",     # 双向等价
            "XOR": "xor",     # 异或
            "xnor": "xnor",   # 同或
            "=": "=",         # 等于
            "<>": "!=",       # 不等于
            "<": "<",         # 小于
            ">": ">",         # 大于
            "<=": "<=",       # 小于等于
            "≥": ">=",        # 大于等于
            "≤": "<=",        # 小于等于
            "+": "+",         # 加
            "-": "-",         # 减
            "*": "*",         # 乘
            "/": "/",         # 除
            "MOD": "MOD",     # 取模
            "DIV": "DIV",     # 整除
            "AG": "AG",       # 全局CTL操作符
            "AF": "AF",       # 最终CTL操作符
            "AX": "AX",       # 下一状态CTL操作符
            "EG": "EG",       # 存在全局CTL操作符
            "EF": "EF",       # 存在最终CTL操作符
            "EX": "EX",       # 存在下一状态CTL操作符
            "G": "G",         # 全局LTL操作符
            "F": "F",         # 最终LTL操作符
            "X": "X",         # 下一状态LTL操作符
            "U": "U",         # 直到
            "R": "R",         # 释放
            "Y": "Y",         # 过去状态
            "Z": "Z",         # 非过去状态
            "H": "H",         # 历史
            "O": "O",         # 一度
        }

        converted_params = {}
        
          # Determine the starting point for parameter mapping
        starting_index = min(int(key) for key in pattern_params.keys())

        for key in pattern_params:
            # Convert numeric key to named key (adjust mapping based on starting index)
            new_key = f"param{int(key) - starting_index + 1}"  # Adjust based on the smallest key

                
            # Remove any prefixes like 'instance.' and replace operators using the replacement dictionary
            expr = pattern_params[key]
            expr = expr.replace("instance.", "")  # 去掉前缀

            # 使用替换库逐个替换操作符
            for old_op, new_op in operator_replacements.items():
                expr = expr.replace(old_op, new_op)
            
            # Assign the converted expression to the new key
            converted_params[new_key] = expr
        
        return converted_params


    # Updated pattern templates for nuXmv
    pattern_templates = {
        "pattern-implication": "AG((PLC_END & ({param1})) -> ({param2}))",
        "pattern-invariant": "AG(PLC_END -> ({param1}))",
        "pattern-forbidden": "AG(PLC_END -> !({param1}))",
        "pattern-statechange-duringcycle": "AG((PLC_START & ({param1})) -> A[!PLC_END U (PLC_END & ({param2}))])",
        "pattern-statechange-betweencycles": "G((PLC_END & ({param1}) & X[!PLC_END U (PLC_END & ({param2}))]) -> X[!PLC_END U (PLC_END & ({param3}))])",
        "pattern-reachability": "EF(PLC_END & ({param1}))",
        "pattern-repeatability": "AG(EF(PLC_END & ({param1})))",
        "pattern-leadsto": "!(E[({param1}) U (PLC_END & !({param2}))])",
        "pattern-leadsto-trigger": "!(E[(PLC_END & ({param1}) & X(PLC_END & ({param2}) & EX(PLC_END & ({param3})))) U (PLC_END & !({param3}))])",
        "pattern-leadsto-earlier": "!(E[(PLC_END & ({param1})) U (PLC_END & !({param2}))])",
        "pattern-timed-trigger": "AG((PLC_END & ({param1})) -> A[!PLC_END U (PLC_END & (T({param1}) >= {param2} & ({param3})))])"
    }

    # Extract the relevant information with safe access
    job_req = property_data.get("property", {}).get("job_req", "")
    pattern_id = property_data.get("property", {}).get("pattern_id", "")
    pattern_params = property_data.get("property", {}).get("pattern_params", {})

    # Check if job_req is "pattern", if pattern_id exists in the template dictionary, and pattern_params is not empty
    if job_req == "pattern" and pattern_id in pattern_templates and pattern_params:
        # Convert pattern_params to named parameters and format expressions
        converted_params = convert_pattern_params(pattern_params)

        # Get the template for the given pattern_id
        template = pattern_templates[pattern_id]
        
        # Fill the template with the corresponding pattern parameters
        filled_model = template.format(**converted_params)
        
        return filled_model
    else:
        # Return empty string if conditions are not met
        return ""


##################### workflow phases #################


def planning_and_feedback(spec, log_file, spec_is_dir=True):
    """
    Performs planning based on the provided specification and handles user feedback.
    To avoid recursive questions, question time is limited to 1.

    Args:
        spec (str): Either a directory containing spec file or a direct user input.
        log_file (str): Log file directory created by create_log_directory to store interaction process.
        spec_is_dir (bool): Determines whether spec is treated as a directory (True) or direct user input (False).

    Returns:
        str: Plan with format of automata from the LLM.
    """
    
    if spec_is_dir:
        # Treat spec as a directory and read the spec file
        spec_path = os.path.join(spec, "spec.txt")  # Assuming 'spec.txt' is the spec file in the directory
        print(f"\nStep 1: Planning, question, and feedback for spec file in directory: {spec_path}")
        
        # Read the specification file as user input
        with open(spec_path, 'r') as spec_file:
            user_msg = spec_file.read()
        print(f"**** User input from spec file: {user_msg}   \
              Notice you should have a detailed plan that can directly write scl code based on it.")
    
    else:
        # Treat spec as a direct user input
        user_msg = spec
        print(f"\nStep 1: Planning, question, and feedback for user input: {user_msg}")
        
    # Read the system message for planning
    planning_sys_msg_path = f"{LLM4PLC_parent_dir}/prompts/phase1/task1_planning"
    with open(planning_sys_msg_path, 'r') as sys_file:
        sys_msg = sys_file.read()
    print(f"System message for planning: {sys_msg}")

    # Call LLM to generate the plan
    plan_result = call_llm(sys_msg, user_msg)

    # Log the planning phase
    log_message(log_file, sys_msg, user_msg, plan_result, "Planning Phase")

    # Extract the plan and question from the response
    plan, question = extract_plan_and_question(plan_result)
    print(f"Extracted Plan: {plan}")
    print(f"Extracted Question: {question}")

    # If LLM proposes a question
    if question:
        print("LLM has posed a question. Awaiting feedback...")
        user_feedback = input_with_timeout("Please provide feedback or answer the question: ", timeout=5)
        
        if user_feedback:
            # Read system message for feedback
            feedback_sys_msg_path = f"{LLM4PLC_parent_dir}/prompts/phase1/task3_feedback"
            with open(feedback_sys_msg_path, 'r') as feedback_sys_file:
                feedback_sys_msg = feedback_sys_file.read()
            print(f"System message for feedback: {feedback_sys_msg}")
            print(f"User feedback: {user_feedback}")
            
            # Call LLM to update the plan based on user response
            feedback_usr_msg = (f"The origin question is: {user_msg}. "
                                f"The previous plan is: {plan}, question is: {question}, "
                                f"and user feedback for question is: {user_feedback}. "
                                "You can update the previous plan for a detailed one, based on which another one can directly write scl code.")
            updated_plan = call_llm(feedback_sys_msg, feedback_usr_msg)
            
            # Log the feedback phase
            log_message(log_file, feedback_sys_msg, user_feedback, updated_plan, "Feedback Phase")
            
            plan = extract_section(updated_plan, "[START_PLAN]", "[END_PLAN]")
            print(f"Updated Plan: {plan}")
            
        # if user have no feedback, proceed with origin plan
    else:
        user_feedback = input_with_timeout("Do you approve the plan? (y/n): ", timeout=5, default="y")

        if user_feedback.lower() == "n":
            print("No feedback provided, moving to the next phase.")
    return plan


def code_gen(spec, plan, log_file, log_dir, max_regenerate_attempts=3, func_call_time=0, spec_is_dir=False):
    """
    Phase 2: Model-based design to generate a compiled ST file for at most {max_regenerate_attempts} times.

    Args:
        plan (str): The plan for code generation generated by step 1.
        log_file (str): Log file directory created by create_log_directory to store interaction process.
        log_dir (str): Log directory created by create_log_directory to store generated ST file content.
        max_regenerate_attempts (int, optional): Maximum number of attempts. Defaults to 3.
        func_call_time (int, optional): the time this function have been called, in order to name the generated st file

    Returns:
        str: Generated SCL code. In case of an empty string output (""), that means the generation process failed.
    """
    
    regenerate_attempts = 0
    compile_output = None
    
    while regenerate_attempts < max_regenerate_attempts:
        # Define the path for the generated SCL file
        scl_file_path = os.path.join(log_dir, f"generated_code_{func_call_time * max_regenerate_attempts + regenerate_attempts + 1}.st")
        print("\nStep 2: Model-based design, generating SCL file")

        # Read the system message for SCL generation
        design_sys_msg_path = f"{LLM4PLC_parent_dir}/prompts/phase2/task1_genSCL"
        with open(design_sys_msg_path, 'r') as design_sys_file:
            design_sys_msg = design_sys_file.read()
        
        print(f"System message for SCL generation: {design_sys_msg}")
        
        # Prepare the input content for the LLM based on the previous attempt
        # if in generation phase, call gen model with llm4plc lora
        # if in fixing phase, call fixing model with llm4plc lora
        if compile_output is None:
            scl_input_content = (f"Origin requirement: {spec}, YOU MUST generate format following the code's head and inside the POU; \
                                 Plan for code: {plan}. "
                                 "Notice you should generate Structured Text code that satisfies the ST format in IEC-61131-3 standard "
                                 "based on the plan.")
            scl_content = call_llm(design_sys_msg, scl_input_content)
        else:
            scl_input_content = (f"Origin requirement: {spec}, YOU MUST generate format following the code's head and inside the POU; \
                                 Plan for code: {plan}, previous generated code: {scl_code}, "
                                 f"compile output for original code: {compile_output}. "
                                 "You should fix and return the FULL code based on the plan and error output that meets ST format in IEC-61131-3 standard."
                                 "THE RETURNED FULL CODE MUST BE STARTED WITH [START_SCL] AND END WITH [END_SCL]")
            scl_content = call_llm(design_sys_msg, scl_input_content)
        
        # Call the LLM to generate SCL content
        # scl_content = call_llm(design_sys_msg, scl_input_content)
        
        # Log the coding phase
        log_message(log_file, design_sys_msg, scl_input_content, scl_content, phase_name="Coding Phase")

        # Extract the SCL code from the generated content
        scl_code = extract_section(scl_content, "[START_SCL]", "[END_SCL]")
        print(f"Generated SCL content: {scl_content}")
        
        if scl_code == scl_content:
            scl_code = extract_section(scl_content, "```", "```")
        
        if scl_code:
            # Save the SCL code to the file
            with open(scl_file_path, 'w') as scl_file:
                scl_file.write(scl_code)
            print(f"SCL file saved at: {scl_file_path}")

            # Compile the SCL file
            # compile_command = f"bash {LLM4PLC_parent_dir}/grammar_check.sh {scl_file_path}"
            compile_command = f"bash {LLM4PLC_parent_dir}/grammar_check_rusty.sh {scl_file_path}"
            print(f"Running compilation command: {compile_command}")

            # Execute the compilation command and capture output
            # the compile_output strictly follow the llm4plc's automation script thus ensuring the correctness of reproduce
            process = subprocess.Popen(compile_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()  # Get standard output and error output
            compile_output = stdout.decode('utf-8') + stderr.decode('utf-8')

            # Print the compilation output for reference
            print(f"Compilation output:\n{compile_output}")
            simple_log_message(f"Compilation output:\n{compile_output}", log_file_path=log_file)
        else:
            compile_output = "no output here"

        # Check the compilation output
        if "SCL output passed compiler validation" in compile_output:
            return scl_code  # Successful generation
        elif "SCL output failed compiler validation" in compile_output:
            regenerate_attempts += 1
            print(f"Error during SCL compilation. Attempt {regenerate_attempts} of {max_regenerate_attempts}.")

            if regenerate_attempts >= max_regenerate_attempts:
                print("Max regeneration attempts exceeded. Code generation failed.")
                return ""  # Generation process terminated
        else:
            # Unexpected output, including no scl content extracted branch
            regenerate_attempts += 1
            print(f"Unexpected compilation result. Attempt {regenerate_attempts} of {max_regenerate_attempts}.")
            
            if regenerate_attempts >= max_regenerate_attempts:
                print("Max regeneration attempts exceeded. Code generation failed.")
                return ""  # Generation process terminated

def verification(scl_content, log_file, log_dir, max_verification_attempts=3, 
                 properties="", func_call_time=0, properties_is_json_list=False):
    """
    Phase 3: Verification, translating the plan and ST code into SMV code and trying to verify 
    for at most {max_verification_attempts} times.

    Args:
        scl_content (str): The ST code to be verified.
        log_file (str): Log file directory created by create_log_directory to store interaction process.
        log_dir (str): Log directory created by create_log_directory to store generated SMV file content.
        max_verification_attempts (int, optional): Maximum number of attempts. Defaults to 3.
        properties (str): Properties to be validated in string format, will be directly appended after the generated SMV file.
        properties_is_json_list (bool): if input properties is a ltl/ctl string or a list of json properties meeting format of plcverif json.
        func_call_time (int, optional): The time this function has been called, in order to name the generated SMV file.

    Returns:
        bool: True if the verification is successful, False if properties are violated, or 
              None if the generation process failed after maximum attempts.
    """
    verification_attempts = 0
    if properties_is_json_list == True:
        property_str = ""
        if properties == "":
            properties = []
        for property in properties:
            property_str += "SPEC\n" + generate_smv_compatible_ltl_ctl_model(property) + "\n"
    else:
        property_str = properties
        
    # print(property_str)
    
    while verification_attempts < max_verification_attempts:
        smv_file_path = os.path.join(log_dir, f"generated_code_verification_{func_call_time * max_verification_attempts + verification_attempts + 1}.smv")
        print("\nStep 3: Verification, generating SMV file")

        # Call LLM to generate SMV file based on SCL content
        verification_sys_msg_path = f"{LLM4PLC_parent_dir}/prompts/phase2/task3_scl2smv"
        with open(verification_sys_msg_path, 'r') as verification_sys_file:
            sys_msg = verification_sys_file.read()
        print(f"System message for SMV generation: {sys_msg}")
        
        
        input_msg = f"scl_content is {scl_content} \
                     properties to be validated: {property_str} \
                    your generated smv file should include the meet the variable definition of these properties, and include PLC_START and PLC_END state. \
                    You only need to generate smv model, these properties will be manually directly added after your smv model "

        # smv_content = call_llm(sys_msg, scl_content)
        smv_content = call_llm(sys_msg, input_msg)
        smv_code = extract_section(smv_content, "[START_SMV]", "[END_SMV]")
        
        # Add properties content after smv_code if properties is not an empty string 
        # if properties:  # Only append if properties is provided
        smv_code += property_str
        
        # Log the verification phase
        log_message(log_file, sys_msg, input_msg, smv_code, phase_name="Verification phase")

        # Save the generated SMV file
        with open(smv_file_path, 'w') as smv_file:
            smv_file.write(smv_code)
        print(f"Generated SMV file saved at: {smv_file_path}")

        # Run nuXmv verification
        verification_result = nuXmv_model_checker(smv_code, smv_file_path)
        print(f"Verification result: {verification_result}")
        
        
        simple_log_message(f"Compilation output:\n{verification_result}", log_file)
        

        if "successful" in verification_result:
            print("Process completed successfully.")
            return True  
        elif "SMV Validation failed" in verification_result:
            print("Process completed with violated properties.")
            return False  
        else:   # Handling unexpected verification results
            verification_attempts += 1
            print(f"Verification failed. Attempt {verification_attempts} of {max_verification_attempts}. Attempting to generate SMV code again.")

            if verification_attempts >= max_verification_attempts:
                print("Max verification attempts exceeded. Verification failed.")
                return None  # Indicate that the verification process failed after maximum attempts

                         
def run_llm_4_plc_1_data(spec, properties, 
                         base_dir="/home/lzh/work/Agents4ICS/LLM_4_PLC_repo/result", 
                         spec_is_path=True, 
                         max_regenerate_attempts=3, 
                         max_verification_attempts=3):
    """
    run llm4plc for 1 time

    Args:
        spec (str): spec content (if spec_is_path=False) or spec dir (if spec_is_path=True)
        properties (list[dict]): a list containing dicts storing multiple properties for system.
        base_dir (_type_): expected base dir for this work, expected LLM_4_PLC_repo/result, and log on this file will be created under it
        spec_is_path (bool, optional): if spec is a path or a file content. Defaults to True.
        max_regenerate_attempts (int, optional): max time for regeneration. Defaults to 3.
        max_verification_attempts (int, optional): max time for verification. Defaults to 3.
    """
    if spec_is_path:
        log_file, log_dir = create_log_directory(spec, base_dir=base_dir)
    else:
        log_file, log_dir = create_log_directory("", base_dir=base_dir)     # spec with dir 
    plan = planning_and_feedback(spec, log_file, spec_is_dir=False)
    design = code_gen(spec, plan, log_file, log_dir, max_regenerate_attempts=max_regenerate_attempts, func_call_time=0)
    if design:          ## plc code passing verification
        verif_result = verification(design, log_file, log_dir, 
                                    max_verification_attempts=max_verification_attempts,
                                    properties=properties,
                                    properties_is_json_list=True)
    else:
        return False  
    
    return verif_result

def run_llm_4_plc(benchmark_dir, max_regenerate_attempts=3, 
                         max_verification_attempts=3):
    # bm_file_path = "/home/lzh/work/Agents4ICS/benckmark/benchmark/kst_medium.txt"
    json_input = parse_plc_instructions(benchmark_dir)
    timestamp = time.strftime("%Y-%m-%d-%H-%M-%S")
    base_dir = f"/home/lzh/work/Agents4ICS/LLM4PLC_reproduce/result/exp_4omini_{timestamp}"
    
    # initialize counter
    true_count = 0
    false_count = 0
    none_count = 0
    
    for i, entry in enumerate(json_input):
        instruction = entry.get("instruction", "")
        properties = entry.get("properties_to_be_validated", "")
        
        # call llm4plc
        result = run_llm_4_plc_1_data(instruction, 
                                       base_dir=f"{base_dir}", 
                                       properties=properties,
                                       max_regenerate_attempts=max_regenerate_attempts, 
                                       max_verification_attempts=max_verification_attempts,
                                       spec_is_path=False)

        # 根据返回值更新计数器
        if result is True:
            true_count += 1
        elif result is False:
            false_count += 1
        elif result is None:
            none_count += 1

    # 打印计数结果
    print(f"Results: True: {true_count}, False: {false_count}, None: {none_count}")

if __name__ == "__main__":
    run_llm_4_plc("/home/lzh/work/Agents4ICS/benchmark/kst_easy_10_9.txt")
    run_llm_4_plc("/home/lzh/work/Agents4ICS/benchmark/kst_medium_10_9.txt")