# supportive tools used in multi_agent system not serving as agent nodes
# Resolve relative path
import sys
from pathlib import Path
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))

from typing import List
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage
from src.langchain_create_agent import create_agent
from src.plcverif import generate_nl_description
import re
from copy import deepcopy
import sys
import os
import json
import numpy as np


def validation_parser(state: List[BaseMessage]):
    """
        combine the following content:
        plan for code agent
        correct code from coding agent
        specs from user_msg
        other safety properties
    """
    def extract_task(doc: str) -> str:
        # Normalize text to lower case to handle case insensitivity
        doc_lower = doc.lower()
        task_start_marker = '[task]'
        task_end_marker = '[task_end]'

        # Check if markers exist
        if task_start_marker in doc_lower and task_end_marker in doc_lower:
            # Extract the content between markers
            start_index = doc_lower.index(task_start_marker) + len(task_start_marker)
            end_index = doc_lower.index(task_end_marker)
            task_content = doc[start_index:end_index].strip()
        else:
            # Call the LLM to interpret and summarize the task
            task_content = call_llm_to_summarize_task(doc)

        return task_content

    def call_llm_to_summarize_task(doc: str) -> str:
        # Here, we'll make a call to the LLM to summarize the task
        # and return the parsed task str
        llm = create_agent(chat_model="deepseek-chat", 
                            system_msg="""
                                You are a helpful assistant to summarize a document to identify what the main task is, \
                                and list out the tasks in the format of:
                                Task 1: (detail of this task)
                                Task 2: (detail of this task)
                                    ...... (continue)
                                Task n: (detail of this task)
                            """,
                            system_msg_is_dir=False)
        input_messages = [
            ("human", f"The document's content is: {doc}"),
        ]
        response = llm.invoke(input_messages)
        return response.content
    
    def extract_st(input_string):
        pattern_scl = '\\[start_scl\\](.*?)\\[end_scl\\]'
        match_scl = re.search(pattern_scl, input_string, re.DOTALL)
        # pattern_smv = '\\[pattern_smv\\](.*?)\\[pattern_smv\\]'
        # match = re.search(pattern_scl, input_string, re.DOTALL)
        if match_scl:
            content = match_scl.group(1)
            return content
        else:
            return input_string
    
    task_info, plan_info, st_code_info = "", "", ""
    for agent_state in state:
        if isinstance(agent_state, HumanMessage):
            # if agent_state.additional_kwargs["agent"] == "user":
            task_info = extract_task(agent_state.content)
        elif isinstance(agent_state, AIMessage):
            if agent_state.additional_kwargs["agent"] == "planning_agent":
                plan_info = agent_state.content
        if task_info != "" and plan_info != "":
            break
    
    # find the last reply from coding agent
    reversed_state = deepcopy(state)
    reversed_state.reverse()
    for agent_state in reversed_state:
        if isinstance(agent_state, AIMessage):
            if agent_state.additional_kwargs["agent"] == "coding_agent":
                st_code_info = extract_st(agent_state.content)
                break
    
    return f"""
                Plan for the generated st code:
                {plan_info}
                Generated st code:
                {st_code_info}                
                User's Task to be realized:
                [task]
                {task_info}
                [task_end]
            """

    
def update_folder_path_in_config(folder_path, config_file_path):
    # read the existing file
    try:
        with open(config_file_path, 'r') as config_file:
            lines = config_file.readlines()
    except FileNotFoundError:
        lines = []

    # remove lines that contain folder_path
    lines = [line for line in lines if 'folder_path' not in line]

    # add the new folder_path
    lines.append(f'folder_path = "{folder_path}"\n')

    # write the new file
    with open(config_file_path, 'w') as config_file:
        config_file.writelines(lines)
     
     
def safe_repr(data):
    """
        A simple function to convert origin output structure to json-format.
    """
    if isinstance(data, str):
        return data
    elif isinstance(data, BaseMessage):
        return data.pretty_repr()
    elif isinstance(data, (dict, list, tuple)):  # Add more if needed 
        return json.dumps(data, indent=2)
    
    return repr(data)
     
def safe_print(data):
    """
        Print result of safe_repr.
    """
    print(safe_repr(data))     


def list_to_json_string(property_list):
    """
    list -> str
    Convert a Python list containing dictionaries to a JSON formatted string.

    Args:
        data_list (list): A list of dictionaries to be converted.

    Returns:
        str: A JSON formatted string representing the input list.
    """
    try:
        # Convert the list to a JSON string with pretty formatting
        json_string = json.dumps(property_list, indent=4, ensure_ascii=False)
        return json_string
    except (TypeError, ValueError) as e:
        print(f"Error: Unable to convert list to JSON string. {e}")
        return ""

def find_and_fulfill_json_str(response_content):
    """
    str -> str
    Extract a JSON string from the response content of property_agent and 
    automatically add descriptions for properties, returning the modified string.
    """
    try:
        # Extract JSON string (assuming it is enclosed in brackets)
        json_start = response_content.find("[")
        json_end = response_content.rfind("]") + 1
        json_string = response_content[json_start:json_end]
        
        # Attempt to parse the JSON string
        properties = json.loads(json_string)
        
        # Iterate over each property in the JSON, performing checks and handling
        for item in properties:
            property_data = item.get("property", {})
            
            # If "job_req" is "pattern" and "pattern_id" and "pattern_params" are known
            if property_data.get("job_req") == "pattern" and "pattern_id" in property_data and "pattern_params" in property_data:
                pattern_id = property_data["pattern_id"]
                pattern_params = property_data["pattern_params"]
                
                # Call the generate_nl_description function to create a natural language description
                nl_description = generate_nl_description(pattern_id, pattern_params)
                
                # Add the generated description to the JSON object
                item["property"]["generated_description"] = nl_description
        
        # Convert the processed JSON object back into a string format
        return json.dumps(properties, indent=4)
    
    except (json.JSONDecodeError, IndexError) as e:
        # If an error occurs during parsing, return the original content or an empty string
        print(f"Error: The content does not contain valid JSON. {e}")
        return ""
  


def parse_plc_file(file_dir):
    if not os.path.isfile(file_dir):
        raise FileNotFoundError("JSON file not found in the directory")
    
    try:
        with open(file_dir, 'r') as file:
            data = json.load(file)
            return data
    except json.JSONDecodeError as e:
        # json parse fail, return as 
        with open(file_dir, 'r') as file:
            original_data = file.read()
        return original_data
    except Exception as e:
        raise IOError(f"An error occurred while reading the file: {e}")
    
# print(parse_plc_file("/home/lzh/work/Agents4PLC-release/benchmark/medium.json"))

### automatically turn json-format data into ltl & ctl sentences
def generate_smv_compatible_ltl_ctl_model(property_data):
    """
    Generates SMV-compatible LTL/CTL model based on the provided job request pattern and pattern ID.

    Args:
        property_data (dict): A dictionary containing the property details, including job_req and pattern_id. (See properties in benchmark)

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
        operator_replacements = {
            "AND": "&",  # AND
            "&&": "&",   # AND
            "∧": "&",    # AND
            "OR": "|",   # OR
            "∨": "|",    # OR
            "NOT": "!",  # NOT
            "¬": "!",    # NOT
            "-->": "->", # Implication
            "→": "->",  # Implication
            "⇒": "->",  # Implication
            "<->": "<->",# Biconditional (if and only if)
            "XOR": "xor", # Exclusive OR
            "xnor": "xnor", # Exclusive NOR
            "=": "=",   # Equal
            "<>": "!=",  # Not equal
            "<": "<",   # Less than
            ">": ">",   # Greater than
            "<=": "<=", # Less than or equal to
            "≥": ">=",  # Greater than or equal to
            "≤": "<=",  # Less than or equal to
            "+": "+",   # Addition
            "-": "-",   # Subtraction
            "*": "*",   # Multiplication
            "/": "/",   # Division
            "MOD": "MOD", # Modulo
            "DIV": "DIV", # Division (integer)
            "AG": "AG",  # Global CTL operator
            "AF": "AF",  # Finally CTL operator
            "AX": "AX",  # Next state CTL operator
            "EG": "EG",  # Exists globally CTL operator
            "EF": "EF",  # Exists finally CTL operator
            "EX": "EX",  # Exists next state CTL operator
            "G": "G",    # Global LTL operator
            "F": "F",    # Finally LTL operator
            "X": "X",    # Next state LTL operator
            "U": "U",    # Until
            "R": "R",    # Release
            "Y": "Y",    # Yesterday (past state)
            "Z": "Z",    # Not yesterday (not past state)
            "H": "H",    # Historical
            "O": "O",    # Once
        }

        converted_params = {}
        
          # Determine the starting point for parameter mapping
        starting_index = min(int(key) for key in pattern_params.keys())

        for key in pattern_params:
            # Convert numeric key to named key (adjust mapping based on starting index)
            new_key = f"param{int(key) - starting_index + 1}"  # Adjust based on the smallest key

                
            # Remove any prefixes like 'instance.' and replace operators using the replacement dictionary
            expr = pattern_params[key]
            expr = expr.replace("instance.", "")  

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

def extract_section(text, start_tag, end_tag):
    """ Helper function to extract content between start and end tags, excluding the tags themselves.
        in case nothing extracted, return the whole content.
        Mainly used to extract and save st or smv or files satisfying certain pattern."""
    start_idx = text.find(start_tag)
    end_idx = text.find(end_tag)

    if start_idx == -1 or end_idx == -1:
        return text

    return text[start_idx + len(start_tag):end_idx].strip()

############### code to convert txt-format benchmark into json format ##############
# this part contain code for converting certain txt-format benchmark 
# which will be actually used in the released version.

def extract_json_substring(text):
    """
    Extracts the first valid JSON array from a given text, supporting parse_plc_instructions.

    Args:
        text (str): The text to search for JSON content.

    Returns:
        str: The extracted JSON substring or None if not found.
    """
    # Match a JSON array, including nested structures
    # pattern = r'(\[.*?\])'  # Match content within the first set of square brackets

    # To ensure we match nested brackets properly, we can count brackets
    depth = 0
    start = None
    for i, char in enumerate(text):
        if char == '[':
            if depth == 0:
                start = i  # Mark the start of the array
            depth += 1
        elif char == ']':
            depth -= 1
            if depth == 0 and start is not None:
                # We've found a complete JSON array
                json_str = text[start:i + 1]
                print(json_str)
                try:
                    json.loads(json_str)  # Verify it's valid JSON
                    return json_str  # Return valid JSON substring
                except json.JSONDecodeError:
                    return None  # If it's not valid JSON

    return None  # No match found 
    
def parse_plc_instructions(file_path):
    """
    Parses a file containing PLC instructions and tests, extracting them into a desired JSON structure.

    Args:
        file_path (str): The path to the file containing the PLC data.

    Returns:
        list: A list of dictionaries where each dictionary contains structured PLC instruction and test data.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    instruction_indices = []
    test_indices = []

    # First loop: Identify the line numbers for instructions and tests
    for idx, line in enumerate(lines):
        # Ignore case and strip whitespace
        if '###instruction' in line.lower():
            instruction_indices.append(idx)
            # If more instructions than tests, append NaN to test_indices
            if len(instruction_indices) > len(test_indices) + 1:
                test_indices.append(np.nan)
        elif '###test' in line.lower():
            test_indices.append(idx)
            # If more tests than instructions, append NaN to instruction_indices
            if len(test_indices) > len(instruction_indices):
                instruction_indices.append(np.nan)

    output_list = []

    # Second loop: Process each instruction-test pair
    for i in range(len(instruction_indices)):
        # Handle instruction block
        current_instruction_start = instruction_indices[i]
        if i < len(test_indices) and isinstance(test_indices[i], int):
            current_test_start = test_indices[i]
        else:
            current_test_start = np.nan

        # Determine instruction content end
        if current_test_start != np.nan and current_test_start > current_instruction_start:
            current_instruction_end = current_test_start
        elif i < len(instruction_indices) - 1:
            current_instruction_end = instruction_indices[i + 1]
        else:
            current_instruction_end = len(lines)

        # Extract instruction content
        if isinstance(instruction_indices[i], int):
            instruction_content = "\n".join(line.strip() for line in lines[current_instruction_start + 1:current_instruction_end]).strip()
        else:
            instruction_content = ""
        
        if i == len(instruction_indices) - 1:
            current_test_end = len(lines)
        elif not isinstance(instruction_indices[i+1], int):
            current_test_end = test_indices[i+1]
        else:
            current_test_end = instruction_indices[i+1]
        
        # Determine test content
        if isinstance(test_indices[i], int):
            # current_test_end = instruction_indices[i + 1] if (i + 1) < len(instruction_indices) else len(lines)
            test_content = "".join(lines[current_test_start + 1:current_test_end]).strip()
            # Extract the valid JSON substring
            properties_to_be_validated = extract_json_substring(test_content)
            if properties_to_be_validated:
                properties_to_be_validated = properties_to_be_validated.replace("\n", "")
                properties_to_be_validated = properties_to_be_validated.replace("\\", "")
                properties_to_be_validated = json.loads(properties_to_be_validated)
        else:
            properties_to_be_validated = "" # No valid test content

        output_list.append({
            "instruction": instruction_content, 
            "properties_to_be_validated": properties_to_be_validated
        })

    return output_list



