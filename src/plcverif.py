## Tools to convert benchmark-compatiable input into multi-dimension plcverif verification process.
## An example is provided in the end about how to use the code for verification on a certain case.

import subprocess
import os
import re
from bs4 import BeautifulSoup
import shutil
from typing import List, Dict
from langchain_openai import ChatOpenAI


def plcverif_validation(st_dir: str, properties_to_be_validated: List[Dict[str, str]],
                        base_dir: str = None):
    summary = []

    base_name = os.path.basename(st_dir).split('.')[0]
    if not base_dir:
        base_dir = f"/home/work/dataset/dataset_runnable_output/{base_name}"

    for i, property in enumerate(properties_to_be_validated, start=1):
        case_id = f"property_{i}"
        output_dir = f"{base_dir}/{case_id}"

        if 'job_req' not in property:
            property = property.get('property', {})  # Update property if not existing

        job_req = property.get("job_req", "assertion")
        pattern_id = property.get("pattern_id")
        pattern_params = property.get("pattern_params", {})
        entry_point = property.get("entry_point", None)

        backend = "nusmv"
        output = plcverif_call(
            source_file=st_dir,
            case_id=case_id,
            job_req=job_req,
            backend=backend,
            pattern_id=pattern_id,
            pattern_params=pattern_params,
            output_dir=output_dir,
            entry_point=entry_point
        )

        # if nusmv fail/timeoutr, switch to  cbmc backend
        if "Timeout" in output or "The NuSMV backend execution has not been successful" in output \
                or 'No suitable files found for further analysis' in output:
            backend = "cbmc"
            print(
                f"nusmv backend failed for case ID: {case_id}. Switching to cbmc backend.")
            output = plcverif_call(
                source_file=st_dir,
                case_id=case_id,
                job_req=job_req,
                backend=backend,
                pattern_id=pattern_id,
                pattern_params=pattern_params,
                output_dir=output_dir,
                entry_point=entry_point
            )

        result_summary = f"property {i}: job_req: {job_req}"

        if backend == "nusmv":
            # handle nusmv/nuXmv backend logic
            smv_cex_file = os.path.join(output_dir, f"{case_id}.smv.cex")
            if os.path.exists(smv_cex_file):
                with open(smv_cex_file, 'r') as f:
                    cex_content = f.read()

                if "is true" in cex_content:
                    result_summary += " is satisfied by the program."
                elif "is false" in cex_content:
                    result_summary += " is violated by the program."
                    # parse counterexample from html and feedback.
                    html_files = [f for f in os.listdir(
                        output_dir) if f.endswith('.html')]
                    if html_files:
                        html_file_path = os.path.join(
                            output_dir, html_files[0])
                        cex_details = parse_html_counterexample(html_file_path)
                        result_summary += "\nCounterexample details:\n" + cex_details
                    else:
                        result_summary += "\nNo counterexample details found."
            else:
                result_summary += "verification could not be completed due to failed smv file generation"

        elif backend == "cbmc":
             # handle cbmc backend logic
            if "VERIFICATION FAILED" in output:
                result_summary += " is violated by the program."
                html_files = [f for f in os.listdir(
                    output_dir) if f.endswith('.html')]
                if html_files:
                    html_file_path = os.path.join(output_dir, html_files[0])
                    cex_details = parse_html_counterexample(html_file_path)
                    result_summary += "\nCounterexample details:\n" + cex_details
                else:
                    result_summary += "\nNo counterexample details found."
                # add cbmc output info to summary
                result_summary += "\ncbmc output info:\n" + output
            elif "No suitable files found for further analysis" in output or "Timeout" in output:
                result_summary += " is not successfully checked."
            elif "VERIFICATION SUCCESSFUL" in output:
                result_summary += " is satisfied by the program."
            else:
                result_summary += " validation result is not clear."

        # summarize pattern details
        if job_req == "pattern":
            result_summary += f"\npattern details:\n{generate_nl_description(pattern_id, pattern_params)}"

        summary.append(result_summary)

    # print overall summary
    print("\n########## Overall Validation Summary ##########\n")
    for item in summary:
        print(item)
    print("\n########## End of Validation Summary ##########\n")
    # return "Plcverif verification result:" + str(summary)
    return summary



def plcverif_call(
    source_file,
    case_id=None,
    job_type='verif',
    backend='nusmv',
    job_req='assertion',
    pattern_id=None,
    pattern_params=None,
    output_dir=None,
    entry_point=None,
    unwind=10,
    verbosity=7
):
    """
    Call plcverif based on the provided parameters
    and return direct execution results.

    Parameters:
    - source_file (str): Path to the source file (required).
    - case_id (str): Identifier for the case (default: extracted from source file name).
    - job_type (str): Type of job, default is 'verif'.
    - backend (str): The backend to use, default is 'nusmv'.
    - job_req (str): Type of request, can be 'assertion' or 'pattern', default is 'assertion'.
    - pattern_id (str): ID of the pattern to check (optional, required if job_req is 'pattern').
    - pattern_params (dict): Dictionary of pattern parameters (optional, required if job_req is 'pattern').
    - output_dir (str): Path to the output directory (default: based on source file).
    - entry_point (str): Optional entry point function or block (optional).
    - unwind (int): Unwind value for CBMC backend (default: 10).
    - verbosity (int): Verbosity level for CBMC backend (default: 7).
    """

    # Determine the case ID based on the source file name if not provided
    if not case_id:
        case_id = os.path.splitext(os.path.basename(source_file))[0]

    # Determine the output directory based on the source file if not provided
    if not output_dir:
        output_dir = f"/home/work/dataset/dataset_runnable_output/{case_id}/"

    # if output_dir exists, just delete content in it.
    if os.path.exists(output_dir):
        print(f"Cleaning up existing output directory: {output_dir}")
        shutil.rmtree(output_dir)

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Determine the path to the backend binary
    if backend == 'nusmv':
        backend_path = os.getenv('nuXmv_PATH', '') + '/nuXmv'
        if not os.path.isfile(backend_path):
            backend_path = subprocess.getoutput('whereis nuXmv').split(' ')[1]
    elif backend == 'cbmc':
        backend_path = os.getenv('CBMC_PATH', '') + '/cbmc'
        if not os.path.isfile(backend_path):
            backend_path = subprocess.getoutput('whereis cbmc').split(' ')[1]
    else:
        raise ValueError("Unsupported backend: {}".format(backend))

    if not os.path.isfile(backend_path):
        raise FileNotFoundError(
            "Backend binary not found at: {}".format(backend_path))

    # Construct the base command
    if backend == 'nusmv':
        cmd = [
            "plcverif-cli",
            "-id", case_id,
            "-job", job_type,
            "-job.backend", backend,
            "-job.backend.binary_path", backend_path,
            "-lf", "step7",
            "-sourcefiles", source_file,
            "-output", output_dir
        ]
    elif backend == 'cbmc':
        cmd = [
            "plcverif-cli",
            "-id", case_id,
            "-job", job_type,
            "-job.backend", backend,
            "-job.backend.binary_path", backend_path,
            "-job.backend.timeout_executor_path", '""',
            "-lf", "step7",
            "-sourcefiles", source_file,
            "-output", output_dir
        ]

    # Handle job_req type
    if job_req == 'assertion':
        cmd.extend(["-job.req", "assertion"])
    elif job_req == 'pattern':
        if not pattern_id or not pattern_params:
            raise ValueError(
                "Pattern ID and parameters are required when job_req is 'pattern'")
        cmd.extend([
            "-job.req", "pattern",
            "-job.req.pattern_id", pattern_id
        ])
        for i, param in enumerate(pattern_params, start=1):
            if "\"" not in pattern_params[param]:
                pattern_params[param] = "\"" + pattern_params[param] + "\""
            cmd.append(f"-job.req.pattern_params.{i}={pattern_params[param]}")
    else:
        raise ValueError("Unsupported job_req: {}".format(job_req))

    # Add entry point if provided
    if entry_point:
        cmd.extend(["-lf.entry", entry_point])

    # Add additional settings for CBMC backend
    if backend == 'cbmc':
        cmd.extend([
            "-job.backend.unwind", str(unwind),
            "-job.backend.verbosity", str(verbosity)
        ])

    # Add reporter format
    cmd.extend(["-job.reporters", "html"])

    print("\n************   Verification process started   ***********")
    print(
        f"Verification completed for case ID: {case_id} with job_req: {job_req}")
    if job_req == 'pattern':
        print(
            f"Patterns to be verified listed as follows:\n{generate_nl_description(pattern_id, pattern_params)}")

    try:
        result = subprocess.run(
            cmd, check=True, capture_output=True, text=True)
        output = result.stdout
        print(output)
        print("************   Verification process completed   ***********\n")

        # the rest parsing will be moved to tool
        if "Output to file" in output:
            return output  

        elif "Timeout" in output or "The NuSMV backend execution has not been successful" in output:
            print(
                f"Verification timed out for case ID: {case_id} with job_req: {job_req}")
            if backend == "cbmc":
                # cbmc timeout means less unwind loops could be needed.
                output = handle_unexpected_output(
                    output_dir, backend, backend_path, int(unwind/2), verbosity)
            return output  

        else:
            print(
                f"Unexpected output for case ID: {case_id} with job_req: {job_req}. Check the logs for details.")
            return handle_unexpected_output(output_dir, backend, backend_path, unwind, verbosity)

    except subprocess.CalledProcessError as e:
        error_output = e.stderr
        print(
            f"Verification failed for case ID: {case_id} with job_req: {job_req}.")
        print(error_output)
        print("************   Verification process completed   ***********\n")
        return error_output
        # if "SettingsParserException" in error_output:
        #     print("Error: The source file does not exist or could not be parsed.")

    # print("************   Verification process completed   ***********\n")


def generate_nl_description(pattern_id, pattern_params):
    """
        Generate natural language description from pattern_id and pattern_params for plcverif input.
        example input:
        {
            '1': "instance.in < instance.tmp", 
            '2': "instance.Q = FALSE AND instance.WIN = FALSE"
        }
        example output:
        If "instance.in < instance.tmp" is true at the end of the PLC cycle, 
        then "instance.Q = FALSE AND instance.WIN = FALSE" should always be true at the end of the same cycle.
    """
    descriptions = {
        "pattern-implication": "If {0} is true at the end of the PLC cycle, then {1} should always be true at the end of the same cycle.",
        "pattern-invariant": "{0} is always true at the end of the PLC cycle.",
        "pattern-forbidden": "{0} is impossible at the end of the PLC cycle.",
        "pattern-statechange-duringcycle": "If {0} is true at the beginning of the PLC cycle, then {1} is always true at the end of the same cycle.",
        "pattern-statechange-betweencycles": "If {0} is true at the end of cycle N and {1} is true at the end of cycle N+1, then {2} is always true at the end of cycle N+1.",
        "pattern-reachability": "It is possible to have {0} at the end of a cycle.",
        "pattern-repeatability": "Any time it is possible to have eventually {0} at the end of a cycle.",
        "pattern-leadsto": "If {0} is true at the end of a cycle, {1} was true at the end of an earlier cycle.",
        "pattern-leadsto-trigger": "If {0} is true at the end of a cycle, there was a change from {1} to {2} at the end of an earlier cycle.",
        "pattern-leadsto-earlier": "If {0} is true at the end of a cycle, {1} was true at the beginning of this or an earlier cycle.",
        "pattern-timed-trigger": "If {0} is true at the end of cycle (EoC), and stays true at EoC for {1} ms of time, {2} will be true."
    }
    if pattern_id in descriptions:
        description_template = descriptions[pattern_id]
        # Use pattern_params.values() to get the values instead of keys
        return description_template.format(*pattern_params.values())
    else:
        return "Unknown pattern ID."


def parse_smv_cex(cex_file_path):
    """
        parse generated .smv.cex file to get specification holds/violated
    """
    try:
        with open(cex_file_path, 'r') as file:
            lines = file.readlines()

        for line in lines:
            if "is true" in line:
                return "satisfied", "The specification is true, indicating the property holds."
            elif "is false" in line:
                return "violated", "The specification is false, indicating the property is violated."

        return "unknown", "No clear success or failure message found in the counterexample file."

    except FileNotFoundError:
        return "error", f"Counterexample file not found: {cex_file_path}"


def parse_html_counterexample(html_file_path):
    """
    Parse generated counterexample from HTML report file to indicate when a specification is violated.
    """
    try:
        with open(html_file_path, 'r') as file:
            soup = BeautifulSoup(file, 'lxml')

        counterexample_details = ""

        # Locate the Counterexample section
        counterexample_section = soup.find('h2', string="Counterexample")
        if counterexample_section:
            table = counterexample_section.find_next('table')
            if table:
                # Append the header for counterexample details
                counterexample_details += "### Counterexample Details:\n\n"

                rows = table.find_all('tr')

                # Iterate through all rows, including headers
                for i, row in enumerate(rows):
                    # Read both headers (th) and data cells (td)
                    cols = row.find_all(['th', 'td'])
                    cols_text = [ele.text.strip() for ele in cols]

                    if cols_text:
                        if i == 0:
                            # Assume first row is the header, format it in Markdown style
                            header_line = " | ".join(cols_text)
                            separator_line = " | ".join(
                                ['---'] * len(cols_text))
                            counterexample_details += f"{header_line}\n{separator_line}\n"
                        else:
                            # Format each row in Markdown style
                            row_line = " | ".join(cols_text)
                            counterexample_details += f"{row_line}\n"
            else:
                counterexample_details += "Counterexample section found, but no details available."

        return counterexample_details or "No counterexample found."

    except FileNotFoundError:
        return f"HTML file not found: {html_file_path}"


def filter_smv_output(output):
    """过滤SMV输出, 移除带有***的无关信息"""
    filtered_lines = [line for line in output.splitlines()
                      if not line.startswith('***')]
    return "\n".join(filtered_lines)

# def filter_cbmc_output(output):
#     """过滤CBMC输出, 保留Results部分"""
#     results_section = False
#     filtered_lines = []

#     for line in output.splitlines():
#         if "Results" in line or "Starting Bounded Model Checking" in line:
#             results_section = True
#         if results_section:
#             filtered_lines.append(line)

#     return "\n".join(filtered_lines)


def filter_cbmc_output(output):
    """过滤CBMC输出, 保留Results部分"""
    filtered_lines = []

    results_found = False
    for line in output.splitlines():
        if "Results" in line:
            results_found = True
            break

    start_keyword = "Results" if results_found else "Starting Bounded Model Checking"

    results_section = False
    for line in output.splitlines():
        if start_keyword in line:
            results_section = True
        if results_section:
            filtered_lines.append(line)

    return "\n".join(filtered_lines)


def add_nan_inf_check(c_code):
    # Define a pattern to find instances of 'nondet_float()' in assignments
    pattern = r'(instance\.[a-zA-Z_]\w*)\s*=\s*nondet_float\(\)\s*;'

    # Function template for checking NaN and Inf
    check_code_template = '''
    while (isnan({var}) || isinf({var})) {{
        {var} = nondet_float();
    }}
    '''

    # Add include for isnan() and isinf() at the top of the file
    if '#include <math.h>' not in c_code:
        c_code = '#include <math.h>\n' + c_code

    # Search and replace all instances of 'nondet_float()' with the check code
    modified_code = re.sub(
        pattern, lambda match: check_code_template.format(var=match.group(1)), c_code)

    return modified_code


def process_c_file(file_path):
    # Read the C file content
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            c_code = file.read()

        # Modify the C code by adding NaN and Inf checks
        modified_c_code = add_nan_inf_check(c_code)

        # Write the modified code back to the file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(modified_c_code)

        print(
            f"File '{file_path}' has been modified to avoid inf and nan checks in c code.")
    except Exception as e:
        print(f"An error occurred: {e}")


def handle_unexpected_output(output_dir, backend, backend_path, unwind, verbosity):
    """
        If the process fails, check if there is useable generated files to continue validation.
        cbmc backend needs this recovery method more often.
    """
    if os.path.exists(output_dir):
        smv_files = [f for f in os.listdir(output_dir) if f.endswith('.smv')]
        c_files = [f for f in os.listdir(output_dir) if f.endswith('.c')]

        if smv_files and backend == 'nusmv':
            print("Running nuXmv on the generated .smv file...")
            result = subprocess.run(f"{backend_path} {os.path.join(output_dir, smv_files[0])}",
                                    shell=True, capture_output=True, text=True)
            filtered_output = filter_smv_output(result.stdout)
            return filtered_output

        elif c_files and backend == 'cbmc':
            print("Running CBMC on the generated .c file...")
            # modify c file so that c inf or nan check
            process_c_file(os.path.join(output_dir, c_files[0]))
            # which is not included in st would not affect result
            try:
                result = subprocess.run(
                    f"{backend_path} {os.path.join(output_dir, c_files[0])} --unwind {unwind} --verbosity {verbosity}",
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=30  # Set a timeout of 30 seconds
                )
                filtered_output = filter_cbmc_output(result.stdout)
            except subprocess.TimeoutExpired:
                filtered_output = "Timeout"
            return filtered_output

        else:
            return "No suitable files found for further analysis."
    else:
        return "Output directory does not exist. No further actions taken."


if __name__ == "__main__":
    properties_to_be_validated = [
            {
                "property_description": "Verify that all assertions are satisfied in the program.",
                "property": {
                    "job_req": "assertion"
                }
            },
            {
                "property_description": "Verify that the relay is updated based on the value of GT1_OUT.",
                "property": {
                    "job_req": "pattern",
                    "pattern_id": "pattern-implication",
                    "pattern_params": {
                        "1": "instance.GT1_OUT = TRUE",
                        "2": "instance.relay = TRUE"
                    },
                    "pattern_description": "If 'instance.GT1_OUT = TRUE' is true at the end of the PLC cycle, then 'instance.relay = TRUE' should always be true at the end of the same cycle."
                }
            },
            {
                "property_description": "Verify that the temp_sensor does not overflow during the FOR loop.",
                "property": {
                    "job_req": "pattern",
                    "pattern_id": "pattern-forbidden",
                    "pattern_params": {
                        "1": "instance.temp_sensor > 32767"
                    },
                    "pattern_description": "'instance.temp_sensor > 32767' is impossible at the end of the PLC cycle."
                }
            },
            {
                "property_description": "Verify that the error flag is not set to FALSE.",
                "property": {
                    "job_req": "pattern",
                    "pattern_id": "pattern-forbidden",
                    "pattern_params": {
                        "1": "instance.error = FALSE"
                    },
                    "pattern_description": "'instance.error = FALSE' is impossible at the end of the PLC cycle."
                }
            }
        ]
    result = plcverif_validation("/home/Agents4ICS/src/test.ST", properties_to_be_validated,
                            base_dir="/home/Agents4ICS/test/base_dir")
