## valid compilers for evaluate part, which is independent with the fixing part.
## only return True or False indicating that compilation passed(True) or failed(False)
## however, if compiler donnot exist, 
import subprocess
import sys
from pathlib import Path
# Resolve the parent directory as an absolute path
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))

import config
import os


def rusty_compiler(file_dir):
    try:
        output = subprocess.check_output(
            f'plc --check {file_dir} 2>&1 | sed "s/\x1b\[[0-9;]*m//g"', 
            shell=True, 
            text=True
        )
        
        if 'error' in output:
            return False
        else:
            return True
    except subprocess.CalledProcessError as e:
        # raise subprocess.CalledProcessError
        return False


def matiec_compiler(file_dir):
    MATIEC_PATH = getattr(config, 'MATIEC_PATH', None)

    if MATIEC_PATH is None:
        MATIEC_PATH = os.getenv('MATIEC_PATH')

    if MATIEC_PATH is None:
        raise ValueError("MATIEC_PATH is not set in config or as an environment variable.")
    
    try:
        output = subprocess.check_output(
            f'iec2iec -f -p "{file_dir}" 2>&1 | head -n -2',
            cwd=MATIEC_PATH,
            shell=True,   # execute in shell
            text=True     # return string
        )
        
        if 'error' in output:
            return False
        else:
            return True
    except subprocess.CalledProcessError as e:
        # raise subprocess.CalledProcessError
        return False
