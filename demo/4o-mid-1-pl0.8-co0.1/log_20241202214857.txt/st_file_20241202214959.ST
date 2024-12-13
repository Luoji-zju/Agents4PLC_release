

(* Define the USER_MAX function block to determine the maximum of two integers *)
FUNCTION_BLOCK USER_MAX
VAR_INPUT
    a : INT;
    b : INT;
END_VAR
VAR_OUTPUT
    max_value : INT;
END_VAR
max_value := a;
IF b > a THEN
    max_value := b;
END_IF;
END_FUNCTION_BLOCK

(* Define the USER_MIN function block to determine the minimum of two integers *)
FUNCTION_BLOCK USER_MIN
VAR_INPUT
    a : INT;
    b : INT;
END_VAR
VAR_OUTPUT
    min_value : INT;
END_VAR
min_value := a;
IF b < a THEN
    min_value := b;
END_IF;
END_FUNCTION_BLOCK

(* Create the FB_ValueComparison function block *)
FUNCTION_BLOCK FB_ValueComparison
VAR_INPUT
    input1 : INT;
    input2 : INT;
    input3 : INT;
    input4 : INT;
    input5 : INT;
    CYCLE : INT;
END_VAR
VAR_OUTPUT
    M : INT;
    N : INT;
    UPDATED_CYCLE : INT;
END_VAR
VAR
    TEMP_MAX_OUT : INT;
    TEMP_MIN_2_OUT : INT;
    TEMP_MIN_3_OUT : INT;
    user_max : USER_MAX;
    user_min : USER_MIN;
END_VAR

(* Calculate TEMP_MAX_OUT using USER_MAX with input2 and input3 *)
user_max(a := input2, b := input3);
TEMP_MAX_OUT := user_max.max_value;

(* Calculate M as the maximum of input1 and TEMP_MAX_OUT *)
user_max(a := input1, b := TEMP_MAX_OUT);
M := user_max.max_value;

(* Calculate TEMP_MIN_2_OUT using USER_MIN with input4 and input5 *)
user_min(a := input4, b := input5);
TEMP_MIN_2_OUT := user_min.min_value;

(* Calculate TEMP_MIN_3_OUT using a complex expression with USER_MIN involving input2, input3, and TEMP_MIN_2_OUT *)
user_min(a := input2, b := input3);
user_min(a := user_min.min_value, b := TEMP_MIN_2_OUT);
TEMP_MIN_3_OUT := user_min.min_value;

(* Calculate N as the minimum of input1 and the sum of TEMP_MIN_3_OUT and input3 *)
user_min(a := input1, b := TEMP_MIN_3_OUT + input3);
N := user_min.min_value;

(* Increment the cycle counter and update UPDATED_CYCLE *)
UPDATED_CYCLE := CYCLE + 1;

END_FUNCTION_BLOCK

