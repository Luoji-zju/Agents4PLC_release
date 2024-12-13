
(* Function Block to calculate the maximum of two integers *)
FUNCTION_BLOCK USER_MAX
VAR_INPUT
    A : INT;
    B : INT;
END_VAR
VAR_OUTPUT
    MAX_OUT : INT;
END_VAR
(* Calculate the maximum value *)
MAX_OUT := IF A > B THEN A ELSE B;
END_FUNCTION_BLOCK

(* Function Block to calculate the minimum of two integers *)
FUNCTION_BLOCK USER_MIN
VAR_INPUT
    A : INT;
    B : INT;
END_VAR
VAR_OUTPUT
    MIN_OUT : INT;
END_VAR
(* Calculate the minimum value *)
MIN_OUT := IF A < B THEN A ELSE B;
END_FUNCTION_BLOCK

(* Main Function Block to compare values and track executions *)
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
    max_func : USER_MAX;
    min_func : USER_MIN;
END_VAR

(* Calculate maximum and minimum values *)
TEMP_MAX_OUT := max_func(A:=input2, B:=input3);
M := max_func(A:=input1, B:=TEMP_MAX_OUT);
TEMP_MIN_2_OUT := min_func(A:=input4, B:=input5);
TEMP_MIN_3_OUT := min_func(A:=input2, B:=TEMP_MIN_2_OUT + input3);
N := min_func(A:=input1, B:=TEMP_MIN_3_OUT);

(* Increment the execution counter *)
UPDATED_CYCLE := CYCLE + 1;

END_FUNCTION_BLOCK

(* Sample program to demonstrate the FB_ValueComparison *)
PROGRAM prg
VAR_INPUT
    input1 : INT := 5;
    input2 : INT := 3;
    input3 : INT := 7;
    input4 : INT := 2;
    input5 : INT := 6;
    CYCLE : INT := 0;
END_VAR

VAR
    fb : FB_ValueComparison;
END_VAR

(* Execute the function block *)
fb(input1 := input1, input2 := input2, input3 := input3, input4 := input4, input5 := input5, CYCLE := CYCLE);

(* Access output values *)
M := fb.M;
N := fb.N;
UPDATED_CYCLE := fb.UPDATED_CYCLE;

END_PROGRAM
