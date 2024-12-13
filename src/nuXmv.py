## python function to assist the nuXmv model checker's verification process.

import re
import subprocess
from config import max_tokens

def nuXmv_model_checker(smv_content, smv_file_path):
    """
        model checking with nuXmv and return verification result.
    """    
    try:
        result = subprocess.run(['nuXmv', smv_file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                                check=True, timeout=10)
    except subprocess.CalledProcessError as e:
        max_len = max_tokens
        err_info = e.stderr.decode()[:max_len] if len(e.stderr) > max_len else e.stderr.decode()
        return f'SMV code compilation failed.\n Origin SMV code: {smv_content}\n CodeError: {err_info}'
    except subprocess.TimeoutExpired as e:
        return f'SMV code execution timeout after 10 seconds.\n Origin smv code: {smv_content}'

    output = result.stdout.decode()

    spec_fail_match = re.search(r'specification .+ is false', output)
    if spec_fail_match:
        index = spec_fail_match.end()
        end_index = output.find('\n', index)
        end_index = output.find('\n', end_index + 1)
        return f'SMV Validation find violated properties: {output[index:end_index].strip()}'

    return 'SMV Validation successful'