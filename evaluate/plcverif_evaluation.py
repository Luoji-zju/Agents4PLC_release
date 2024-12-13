from pathlib import Path
import os
import sys
import json
import numpy as np
import subprocess

# Resolve the parent directory as an absolute path
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))

# from LangChain.multi_agents import multi_agent_workflow
from src.plcverif import plcverif_validation
from src.compiler import matiec_compiler, rusty_compiler
from evaluate.pretty_summary import summary
from config import *
from datetime import datetime

import config
evaluate_compiler = getattr(config, 'evaluate_compiler', 'rusty')
plcverif_verified_threshold = getattr(config, 'plcverif_verified_threshold', 0.80)
plcverif_passed_threshold = getattr(config, 'plcverif_passed_threshold', 0.80)

def load_json_from_file(file_path):
    """
    Load JSON data from a file.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        list or None: Parsed JSON data or None if an error occurs.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            print(f"Successfully loaded JSON data from {file_path}")
            return data
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")

    return None


def single_file_plcverif_evaluation(st_file_path, folder_path, properties):
    """
        evaluate if generated st file actually pass.
        input value:
        st_file_path (for syntax checking)
        properties (for semantics checking)
        log_file_path (for storing temp content in checking process)
        
        output:
        bool: if syntax checking fails
        dict: validation_statistics
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Directory created: {folder_path}")
    else:
        print(f"Directory already exists: {folder_path}")
    
    try:
        output = subprocess.check_output(
            f'plc --check {st_file_path} 2>&1 | sed "s/\x1b\[[0-9;]*m//g"', 
            shell=True, 
            text=True
        )
        
        if 'error' in output:
            return False, None
    except subprocess.CalledProcessError as e:
        return False, None
    
    validation_result = plcverif_validation(st_file_path, properties, base_dir=f"{folder_path}")
    
    validation_statistics = {              # Statistics for different property validation statuses
        "success": 0,                # Count of properties that passed validation
        "failure": 0,                # Count of properties that failed validation
        "not_verified": 0,            # Count of properties that were not verified
        "total": len(validation_result)
    }
    for property_str in validation_result:
        if "violated" in property_str:
            validation_statistics["failure"] += 1
        elif "satisfied" in property_str:
            # Property verification succeeded
            validation_statistics["success"] += 1
        else:
            # Unverified property
            validation_statistics["not_verified"] += 1
            
    if validation_statistics["success"] > plcverif_passed_threshold * validation_statistics["total"]: # more than thres satisfy property
        return True
    elif validation_statistics["not_verified"] <= (1 - plcverif_verified_threshold) * validation_statistics["total"]: # less or eq than (1-thres) not verified
        return False
    else:
        return None
    
def plcverif_evaluation(input_files, base_dir):
    """_summary_

    Args:
        Here is the minimal structure for item in input_files, which is just the minimal output format of your multi agent work flow
        however you realize it:
        
        {
            "st_file_path": str,   # Dictionary to record generated ST file paths and their validation status.
            "properties": prop_content  # properties copied from origin benchmark.
            # "eval_folder_path": str,     
            # evaluate log folder. Recommended to be reserved since auto-generated like /root_folder_path/{st_file_name}_{timestamp}.
        }
        
        base_dir: dir to store evaluation temp results.
    
        However based on our multi-agent system the following content 
        are generated and input_files (_type_) is list of log summaries like:\
        {
            "st_file_path": "",
            "compilation_passing": "",       # Compilation status: True (success), False (failure), "" (not validated)
            "property_stats": {              # Statistics for different property validation statuses
                "success": 0,                # Count of properties that passed validation
                "failure": 0,                # Count of properties that failed validation
                "not_verified": 0            # Count of properties that were not verified
                "total": len(validation_result) # all property counts
            },
            "folder_path":                   # log folder
            "log_file_path":
            "instruction": inst_content,
            "properties": prop_content
        }
        
    This function will directly print out validation result and thereby write into log file if dir provided.
    
    Here, Pass >= plcverif_passed_threshold cases in verification will be considered syntactic checking "passed", 
    and verified >= plcverif_verified_threshold cases in verification will be considered "validation_satisfied", 
    because of the fact that some auto-generated properties could be failed 
    due to strange reasons of plcverif because of the limitation of the tool itself, that donnot mean the failure of the 
    semantics checking. See config to adjust hyperparams. 
    
    """
    # Initialize statistics dictionary
    compilation_validation_statistics = {
        "compilation_success": 0,  # Count of properties that passed validation
        "verified": 0,        # Count of properties that passed validation but not verified
        "validation_satisfied": 0, # Count of properties that were not verified
        "valid_inputs": 0,         # Count of valid input files
        "total": len(input_files)  # Total number of input files
    }
    
    valid_input_files = []
    verif_files = []

    # step 0: check valid inputs
    # if following minimal input format, auto-gen "eval_folder_path" thus append to valid_input_files 
    for file in input_files:
        if ("st_file_path" in file) and isinstance(file["st_file_path"], str): 
            st_file_name_without_ext = os.path.splitext(os.path.basename(file["st_file_path"]))[0]
            timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
            file["eval_folder_path"] = os.path.join(base_dir, f"{st_file_name_without_ext}_{timestamp}")
            print(file)
        # Check if the file has all required keys and if the properties are valid
        if ("eval_folder_path" in file and "properties" in file and 
            isinstance(file["eval_folder_path"], str) and 
            hasattr(file["properties"], "__iter__")):  
            # If the file meets the requirements, add it to the valid list and increment the counter
            valid_input_files.append(file)
            compilation_validation_statistics["valid_inputs"] += 1
            
            
    # step 1: compiling using compiler
    for input_file in input_files:
        if evaluate_compiler == "matiec":
            compile_result = matiec_compiler(input_file["st_file_path"])
        elif evaluate_compiler == "rusty":
            compile_result = rusty_compiler(input_file["st_file_path"])
        else:
            compile_result = rusty_compiler(input_file["st_file_path"])
            
        if compile_result:
            compilation_validation_statistics["compilation_success"] += 1
            verif_files.append(input_file)
    
        # step 2: automated verification
    for verif_file in verif_files:
        verif_result = single_file_plcverif_evaluation(input_file["st_file_path"], input_file["eval_folder_path"], input_file["properties"])
        if verif_result is not None:
            compilation_validation_statistics["verified"] += 1
            if verif_file == True:
                compilation_validation_statistics["validation_satisfied"] += 1
           
    summary(compilation_validation_statistics, base_dir=base_dir)     
    # print(compilation_validation_statistics)


if __name__ == "__main__":
    st_file_path = "/home/lzh/work/Agents4PLC-release/benchmark/test.ST"
    folder_path = "/home/lzh/work/Agents4PLC-release/result/plcverif_evaluation"
    properties = [
            {
                "property_description": "Verify that all assertions are satisfied in the program.",
                "property": {
                    "job_req": "assertion"
                }
            },
            {
                "property_description": "Verify that the motor is not considered critical if the pressure is above or equal to the threshold.",
                "property": {
                    "job_req": "pattern",
                    "pattern_id": "pattern-implication",
                    "pattern_params": {
                        "1": "instance.Pressure_LOW >= 36464",
                        "2": "instance.Motor_Critical = FALSE"
                    },
                    "pattern_description": "If 'instance.Pressure_LOW >= 36464' is true at the end of the PLC cycle, then 'instance.Motor_Critical = FALSE' should always be true at the end of the same cycle."
                }
            },
            {
                "property_description": "Verify that the pressure values are within safe ranges.",
                "property": {
                    "job_req": "pattern",
                    "pattern_id": "pattern-invariant",
                    "pattern_params": {
                        "1": "instance.Pressure_LOW >= 0 AND instance.Pressure_LOW <= 65535"
                    },
                    "pattern_description": "'instance.Pressure_LOW >= 0 AND instance.Pressure_LOW <= 65535' is always true at the end of the PLC cycle."
                }
            }
        ]
    input_files = [
        {
            "st_file_path": st_file_path,   # Dictionary to record generated ST file paths and their validation status.
            # "folder_path": folder_path,     # log folder. Recommended to be auto-generated like /root_folder_path/{st_file_name}_{timestamp}.
            "properties": properties  # properties copied from origin benchmark.
        }
    ]
    plcverif_evaluation(input_files, folder_path)

    # # Print results with one decimal place
    # print(f"Total files: {all_number}, Syntax compilation passed: {compilation_validation_statistics["compilation_success"]}")
    # print(f"Pass >= 80% properties: {pass_thres_080_num}, Pass >= 50% properties: {pass_thres_050_num}")
    # print(f"Verified >= 80% properties: {verified_thres_080_num}")

    # # Optionally, write the statistics to a file in the base directory
    # if base_dir:
    #     file_path = os.path.join(base_dir, "evaluation_summary.txt")
    #     with open(file_path, "w") as f:
    #         f.write(f"Total files: {all_number}\n")
    #         f.write(f"Syntax compilation passed: {compilation_validation_statistics["compilation_success"]}/{all_number} "
    #                 f"({compilation_validation_statistics["compilation_success"]/all_number:.1%})\n")
    #         f.write(f"Pass >= 80% properties: {pass_thres_080_num}/{compilation_validation_statistics["compilation_success"]} "
    #                 f"({pass_thres_080_num/compilation_validation_statistics["compilation_success"]:.1%})\n")
    #         f.write(f"Pass >= 50% properties: {pass_thres_050_num}/{compilation_validation_statistics["compilation_success"]} "
    #                 f"({pass_thres_050_num/compilation_validation_statistics["compilation_success"]:.1%})\n")
    #         f.write(f"Verified >= 80% properties: {verified_thres_080_num}/{compilation_validation_statistics["compilation_success"]} "
    #                 f"({verified_thres_080_num/compilation_validation_statistics["compilation_success"]:.1%})\n")

    #     # Write input_files content to a separate file
    #     log_summaries_file_path = os.path.join(base_dir, "input_files.txt")
    #     with open(log_summaries_file_path, "w") as log_file:
    #         try:
    #             # Try to dump as JSON string
    #             summaries_str = json.dumps(input_files, indent=4)
    #         except (TypeError, ValueError):
    #             # If it fails, use repr() to convert the object to a string
    #             summaries_str = repr(input_files)
            
    #         log_file.write(summaries_str)

            


    


# if __name__ == "__main__":
#     # Determine the source for JSON input
#     # json_file_path = '/home/lzh/work/dataset/dataset_raw/test.json'
#     # bm_file_path = "/home/lzh/work/Agents4ICS/benchmark/benchmark/test.txt"
#     json_file_path = "/home/lzh/work/Agents4ICS/benchmark/benchmark/test.json"
    
#     # experiment setting: read from benchmark dataset
#     # json_input = parse_plc_instructions(bm_file_path)
#     json_input = load_json_from_file(json_file_path)
    
#     if json_input is not None:
#         # Run the batch process on the JSON input
#         results = batch_run_json_dataset(json_input)

#         # Output the results
#         for result in results:
#             print(f"Instruction:\n{result['instruction']}\nGenerated Output:\n{result['output']}\n")
