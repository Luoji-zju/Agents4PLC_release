import os
import time
import subprocess
import re
import os
import threading

from pathlib import Path
import sys
import os
import json

# Resolve the parent directory for whole program and llm4plc itself as an absolute path
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))

LLM4PLC_parent_dir = Path(__file__).resolve().parent
# sys.path.append(str(LLM4PLC_parent_dir))

from config import chat_model, reasoning_model, max_tokens, efficiency_rounds

# translate json format property into smv compatiable ltl/ctl formula / parse property from json file
from src.tools import generate_smv_compatible_ltl_ctl_model, parse_plc_file, extract_section

from src.simple_call_llm import call_llm

############# function tools #################

def nuXmv_model_checker(smv_content, smv_file_path, timeout=10):
    """
        model checking with nuXmv and return verification result.
    """
    try:
        result = subprocess.run(
            ['nuXmv', smv_file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            timeout=timeout  
        )
    except subprocess.CalledProcessError as e:
        max_len = 1000 
        err_info = e.stderr.decode()[:max_len] if len(e.stderr) > max_len else e.stderr.decode()
        return f'SMV code compilation failed.\n Origin SMV code: {smv_content}\n CodeError: {err_info}'
    except subprocess.TimeoutExpired as e:
        return f'The process exceeded the time limit of {timeout} seconds and was terminated.\n Origin SMV code: {smv_content}'


    output = result.stdout.decode()

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
    plan_result = call_llm(sys_msg, user_msg, chat_model=reasoning_model)

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
            updated_plan = call_llm(feedback_sys_msg, feedback_usr_msg, chat_model=reasoning_model)
            
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


def code_gen(spec, plan, log_file, log_dir, func_call_time=0, spec_is_dir=False):
    """
    Phase 2: Single attempt code generation
    
    Returns:
        tuple: (success: bool, scl_code: str, scl_file_path: str)
    """
    scl_file_path = os.path.join(log_dir, f"generated_code_{func_call_time}.st")
    print("\nStep 2: Model-based design, generating SCL file")

    # Read system message
    design_sys_msg_path = f"{LLM4PLC_parent_dir}/prompts/phase2/task1_genSCL"
    with open(design_sys_msg_path, 'r') as design_sys_file:
        design_sys_msg = design_sys_file.read()
    
    # Generate SCL content
    scl_input_content = (f"Origin requirement: {spec}, YOU MUST generate format following the code's head and inside the POU; "
                         f"Plan for code: {plan}. Notice you should generate Structured Text code that satisfies the ST format "
                         "in IEC-61131-3 standard based on the plan.")
    
    scl_content = call_llm(design_sys_msg, scl_input_content)
    log_message(log_file, design_sys_msg, scl_input_content, scl_content, phase_name="Coding Phase")

    # Extract SCL code
    scl_code = extract_section(scl_content, "[START_SCL]", "[END_SCL]")
    if scl_code == scl_content:  # Fallback extraction
        scl_code = extract_section(scl_content, "```", "```")
    
    # Save and compile
    with open(scl_file_path, 'w') as scl_file:
        scl_file.write(scl_code or "")
    
    compile_command = f"bash {LLM4PLC_parent_dir}/grammar_check_rusty.sh {scl_file_path}"
    process = subprocess.Popen(compile_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    compile_output = stdout.decode('utf-8') + stderr.decode('utf-8')
    
    # success = "SCL output passed compiler validation" in compile_output
    if "SCL output passed compiler validation" in compile_output:
        success = True
    elif "SCL output failed compiler validation" in compile_output:
        success = False
        print(f"Error during SCL compilation.")
    else:
        print(f"Unexpected compilation result.")
    return success, scl_code, scl_file_path

def verification(scl_content, log_file, log_dir, properties="", func_call_time=0, properties_is_json_list=False):
    """
    Single verification attempt
    
    Returns:
        tuple: (result: bool, smv_file_path: str) 
               - True: verification passed
               - False: properties violated
               - None: verification failed
    """
    smv_file_path = os.path.join(log_dir, f"generated_code_verification_{func_call_time}.smv")
    
    # Generate properties
    if properties_is_json_list:
        property_str = "\n".join([f"SPEC\n{generate_smv_compatible_ltl_ctl_model(p)}" for p in properties])
    else:
        property_str = properties

    # Generate SMV
    verification_sys_msg_path = f"{LLM4PLC_parent_dir}/prompts/phase2/task3_scl2smv"
    with open(verification_sys_msg_path, 'r') as f:
        sys_msg = f.read()
    
    input_msg = (f"scl_content: {scl_content}\nproperties to validate: {property_str}\n"
                 "Generate SMV model with PLC_START/PLC_END states and variable definitions matching the properties.")
    
    smv_content = call_llm(sys_msg, input_msg)
    smv_code = extract_section(smv_content, "[START_SMV]", "[END_SMV]") + property_str
    
    # Save and verify
    with open(smv_file_path, 'w') as f:
        f.write(smv_code)
    
    verification_result = nuXmv_model_checker(smv_code, smv_file_path)
    
    # Parse result
    if "successful" in verification_result:
        return True, smv_file_path
    elif "violated" in verification_result:
        return False, smv_file_path
    else:
        return None, smv_file_path

def run_llm_4_plc_1_time(spec, properties, 
                        base_dir="/result", 
                        spec_is_path=True,
                        efficiency_rounds=5):
    """
    新版执行逻辑：
    1. 总尝试次数由efficiency_rounds控制
    2. 维护状态机根据验证结果决定下一步操作
    3. 完整记录所有生成的SCL文件路径
    """
    # 初始化日志
    if spec_is_path:
        log_file, log_dir = create_log_directory(spec, base_dir)
    else:
        log_file, log_dir = create_log_directory("manual_spec", base_dir)
    
    # 阶段1：生成计划
    plan = planning_and_feedback(spec, log_file, spec_is_dir=False)
    
    scl_paths = []
    current_scl = None
    verification_round = 0
    total_rounds = 0
    need_code_gen = True  # 初始需要生成代码

    while total_rounds < efficiency_rounds:
        if need_code_gen:
            # 代码生成阶段
            gen_idx = len(scl_paths)
            success, code, path = code_gen(
                spec, plan, log_file, log_dir,
                func_call_time=gen_idx
            )
            # scl_paths.append(path)
            # current_scl = code if success else None
            if success:
                current_scl = code
                need_code_gen = False
            total_rounds += 1
        else:
            # 验证阶段
            verif_result, _ = verification(
                current_scl, log_file, log_dir,
                properties=properties,
                func_call_time=verification_round,
                properties_is_json_list=True
            )
            total_rounds += 1
            verification_round += 1

            if verif_result is False:
                need_code_gen = True
                verification_round = 0
            elif verif_result is True:
                break
            
        scl_paths.append(path)

    # 保持与原返回格式兼容，但scl_file_path改为列表
    return scl_paths, properties

timestamp = time.strftime("%Y-%m-%d-%H-%M-%S")
def run_llm_4_plc(benchmark_dir, max_regenerate_attempts=3, 
                         max_verification_attempts=3,
                         base_dir = f"/home/Agents4ICS/LLM4PLC_reproduce/result/exp_{timestamp}"):
    # bm_file_path = "/home/lzh/work/Agents4ICS/benckmark/benchmark/kst_medium.txt"
    json_input = parse_plc_file(benchmark_dir)

    result_list = []  

    for i, entry in enumerate(json_input):
        instruction = entry.get("instruction", "")
        properties = entry.get("properties_to_be_validated", "")
        
        # call llm4plc
        scl_file_path, properties = run_llm_4_plc_1_time(instruction, 
                                       base_dir=f"{base_dir}", 
                                       properties=properties,
                                    #    max_regenerate_attempts=max_regenerate_attempts, 
                                    #    max_verification_attempts=max_verification_attempts,
                                       spec_is_path=False)
        
        result_dict = {
            "st_file_path": scl_file_path,   
            "properties": properties         
        }
        
        print(result_dict)
        
        result_list.append(result_dict)  
    
    filename = f"{base_dir}/result.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(result_list, f, ensure_ascii=False, indent=4)
        
    return base_dir

### function for efficiency study
# def run_llm_4_plc_efficiency(benchmark_dir, max_regenerate_attempts=efficiency_rounds, 
#                          max_verification_attempts=3,
#                          base_dir = f"/home/Agents4ICS/LLM4PLC_reproduce/result/exp_{timestamp}"):
#     # bm_file_path = "/home/lzh/work/Agents4ICS/benckmark/benchmark/kst_medium.txt"
#     json_input = parse_plc_file(benchmark_dir)

#     result_list = []  

#     for i, entry in enumerate(json_input):
#         instruction = entry.get("instruction", "") 
#         properties = entry.get("properties_to_be_validated", "")
        
#         # call llm4plc
#         scl_file_path, properties = run_llm_4_plc_1_time(instruction, 
#                                        base_dir=f"{base_dir}", 
#                                        properties=properties,
#                                        max_regenerate_attempts=max_regenerate_attempts, 
#                                        max_verification_attempts=max_verification_attempts,
#                                        spec_is_path=False)
        
#         result_dict = {
#             "st_file_path": scl_file_path,   
#             "properties": properties         
#         }
        
#         # print(result_dict)
        
#         result_list.append(result_dict)  
    
#     filename = f"{base_dir}/result.json"
#     with open(filename, 'w', encoding='utf-8') as f:
#         json.dump(result_list, f, ensure_ascii=False, indent=4)
        
#     return base_dir

if __name__ == "__main__":

    input_dir = f"{parent_dir}/benchmark/just4test_1.json"
    output_dir = f"{parent_dir}/result/LLM4PLC_reproduce/question1.json"
    
    # json_input = parse_plc_file("/home/lzh/work/Agents4PLC-release/benchmark/test.json")
    # spec = json_input[0]["instruction"]
    # properties = json_input[0]['properties_to_be_validated']
    
    run_llm_4_plc(input_dir)
    