## program to run multi agent frameworks and evaluate for results.

import sys
from pathlib import Path
# Resolve the parent directory as an absolute path
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))

import traceback
from datetime import datetime
from evaluate.smv_evaluation import smv_evaluation
from evaluate.plcverif_evaluation import plcverif_evaluation

def batch_run_json_dataset(json_data):
    """
    Takes JSON input and processes the multi_agent_workflow for each instruction in the JSON data.

    Args:
        json_data (list): A list of dictionaries containing parsed instructions and their properties.
        The json_data input should be json compatiable and each item should include 
        "instruction" and "properties_to_be_validated" subitems.

    Returns:
        list: A list of dictionaries with instructions and their corresponding workflow outputs.
    """

    input_files = []
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    base_dir = f"{str(parent_dir)}/result/experiment_{timestamp}"
    
    for entry in json_data:
        instruction = entry.get("instruction", "")
        properties = entry.get("properties_to_be_validated", "")
        instruction += "You must strictly follow the format of given content.\
                        Any other content should not be added here."
        
        if instruction:
            try:
                print(f"Processing instruction: {instruction}")
                log_summary = multi_agent_workflow(instruction, properties, is_path=False, base_dir=base_dir)
                log_summary["instruction"] = instruction
                log_summary["properties"] = properties
                input_files.append(log_summary)
            except Exception as e:
                error_message = traceback.format_exc()
                print(f"Error occurred while processing instruction '{instruction}': {error_message}")
        else:
            print("No instruction found, skipping.")
            
    batch_evaluation(input_files, base_dir=base_dir)