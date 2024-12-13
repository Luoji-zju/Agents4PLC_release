## Description on evaluation scripts

Now evaluation scripts is separated from origin evaluation code. Despite that evaluation code could be similar to their
brothers in "validation agent", the evaluation process is separated from the origin workflow's verification-fixing loop
and serve as an independent process to finally judge the result of verification.

```
/direct_smv_verification.py
/plcverif_evaluation.py
```

New tools for evaluation can be added later. However, the "Protocol" for evaluation programs should follow:

Input : minimal structure for the input format should be a list like:
[
    {
        "st_file_path": str,   # Dictionary to record generated ST file paths and their validation status.
        "folder_path": str,         # log folder. Recommended to be auto-generated like /root_folder_path/{st_file_name}_{timestamp}.
        "properties": prop_content  # properties copied from origin benchmark.
    }
]

Output: statistics about program verification in the format of {number in class/all_number/ratio}. for example:

f"Total files: {all_number}"
f"Syntax compilation passed: {syntax_compilation_num}/{all_number} "
                    f"({syntax_compilation_num/all_number:.1%})"
f"Pass >= 80% properties: {pass_thres_080_num}/{syntax_compilation_num} "
                    f"({pass_thres_080_num/syntax_compilation_num:.1%})\n")
f"Pass >= 50% properties: {pass_thres_050_num}/{syntax_compilation_num} "
                    f"({pass_thres_050_num/syntax_compilation_num:.1%})\n")
f"Verified >= 80% properties: {verified_thres_080_num}/{syntax_compilation_num} "
                    f"({verified_thres_080_num/syntax_compilation_num:.1%})\n")