## verification based on direct verification following LLM4PLC[https://dl.acm.org/doi/abs/10.1145/3639477.3639743].
## LLM based auto smv code generation from st file + auto translator from plcverif-compatiable 
## json list to smv compatiable ltl/ctl formula.
## note that this way follow the origin LLM4PLC's idea, using (maybe fine-tuned) LLM to translate ST to SMV for verification.
## therefore, the incosistency between st and smv model could affect the accuracy of evaluation.
## (however, to reproduce it, such way is necessary.)

import sys
from datetime import datetime
import os
from pathlib import Path

# Resolve the parent directory for whole program and llm4plc itself as an absolute path
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))

LLM4PLC_parent_dir = f"{parent_dir}/LLM4PLC_reproduce"

from src.tools import generate_smv_compatible_ltl_ctl_model, extract_section
from src.simple_call_llm import call_llm
from src.nuXmv import nuXmv_model_checker
from src.compiler import rusty_compiler, matiec_compiler
from evaluate.pretty_summary import summary
import config
evaluate_compiler = getattr(config, 'evaluate_compiler', None)

def single_file_smv_evaluation(st_file_path, folder_path, properties):
    """
    Returns:
        bool: True if the verification is successful, False if properties are violated, or 
              None if the smv file is not recognized meaning timeout due to space explosion or incorrect generated smv syntax.
    """
    # read content from st file.
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Directory created: {folder_path}")
    else:
        print(f"Directory already exists: {folder_path}")
    
    try:
        with open(st_file_path, 'r') as file:
            scl_content = file.read()
    except FileNotFoundError:
        print(f"Error: The file at {st_file_path} was not found.")
    except PermissionError:
        print(f"Error: Permission denied when trying to read the file at {st_file_path}.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
    
    smv_file_path = os.path.join(folder_path, f"smv_verification.smv")
    log_file_path = os.path.join(folder_path, f"log.txt")

    # Call LLM to generate SMV file based on SCL content
    verification_sys_msg_path = f"{LLM4PLC_parent_dir}/prompts/phase2/task3_scl2smv"
    with open(verification_sys_msg_path, 'r') as verification_sys_file:
        sys_msg = verification_sys_file.read()
    print(f"System message for SMV generation: {sys_msg}")
    
    
    properties_str = "\n"
    if len(properties) > 0:
        if properties == "":
            properties = []
        for property in properties:     # by default the plcverif formulas are all CTL specs.
            prop_str = generate_smv_compatible_ltl_ctl_model(property)
            if prop_str:
                properties_str += "SPEC\n" + prop_str + "\n"
            
    
    input_msg = f"scl_content is {scl_content} \
                    properties to be validated: {properties_str} \
                your generated smv file should include the meet the variable definition of these properties, and include PLC_START and PLC_END state. \
                You only need to generate smv model, these properties will be manually directly added after your smv model "

    smv_content = call_llm(sys_msg, input_msg)
    smv_code = extract_section(smv_content, "[START_SMV]", "[END_SMV]")
    
    # # Add properties content after smv_code if properties is not an empty string 
    # # if properties:  # Only append if properties is provided
    smv_code += properties_str
    
    # print(smv_code)
    
    # Save the generated SMV file
    with open(smv_file_path, 'w') as smv_file:
        smv_file.write(smv_code)
    print(f"Generated SMV file saved at: {smv_file_path}")
    

    # Run nuXmv verification
    verification_result = nuXmv_model_checker(smv_code, smv_file_path)
    
    with open(log_file_path, 'w') as log_file:
        log_file.write(verification_result)
    print(f"Verification result saved at: {log_file_path}")
    
    if "fail" in verification_result:
        return None
    elif "violated" in verification_result:
        return False
    elif "successful" in verification_result:
        return True
    
    return None
    
            
def smv_evaluation(input_files, base_dir):
    """
    Evaluates the input files based on the provided structure and criteria.

    Input: input_files: A list of dictionaries with the following minimal structure:
    [
        {
            "st_file_path": str,   # Dictionary to record generated ST file paths and their validation status.
            "properties": prop_content  # properties copied from origin benchmark.
            # "eval_folder_path": str,     
            # evaluate log folder. Recommended to be reserved since auto-generated like /base_dir/{st_file_name}_{timestamp}.
        }
    ]
    base_dir: dir to store evaluation temp results.
    Note: Only files with all passed properties will be considered "validation_satisfied".
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
        verif_result = single_file_smv_evaluation(input_file["st_file_path"], input_file["eval_folder_path"], input_file["properties"])
        if verif_result is not None:
            compilation_validation_statistics["verified"] += 1
            if verif_file == True:
                compilation_validation_statistics["validation_satisfied"] += 1
                
    print(compilation_validation_statistics)

    

            
if __name__ == "__main__":
    st_file_path = "/home/lzh/work/Agents4PLC-release/benchmark/test.ST"
    folder_path = "/home/lzh/work/Agents4PLC-release/result/evaluation"
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
    smv_evaluation(input_files, folder_path)
