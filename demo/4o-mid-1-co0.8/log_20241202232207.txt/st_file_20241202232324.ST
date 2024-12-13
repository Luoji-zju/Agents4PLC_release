
(* Define function block for calculating maximum and minimum values with a cycle counter increment. *)

(* Auxiliary function block for calculating the maximum of two integers *)
FUNCTION_BLOCK USER_MAX
VAR_INPUT
    A : INT;
    B : INT;
END_VAR
VAR_OUTPUT
    MAX_OUT : INT;
END_VAR
(* Compare inputs and assign the maximum value to MAX_OUT *)
MAX_OUT := A;
IF B > A THEN
    MAX_OUT := B;
END_IF;
END_FUNCTION_BLOCK

(* Auxiliary function block for calculating the minimum of two integers *)
FUNCTION_BLOCK USER_MIN
VAR_INPUT
    A : INT;
    B : INT;
END_VAR
VAR_OUTPUT
    MIN_OUT : INT;
END_VAR
(* Compare inputs and assign the minimum value to MIN_OUT *)
MIN_OUT := A;
IF B < A THEN
    MIN_OUT := B;
END_IF;
END_FUNCTION_BLOCK

(* Main function block for value comparison and cycle increment *)
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
    max_block : USER_MAX;
    min_block : USER_MIN;
END_VAR

(* Calculate TEMP_MAX_OUT - maximum of input2 and input3 *)
max_block(A := input2, B := input3);
TEMP_MAX_OUT := max_block.MAX_OUT;

(* Calculate M - maximum of input1 and TEMP_MAX_OUT *)
max_block(A := input1, B := TEMP_MAX_OUT);
M := max_block.MAX_OUT;

(* Calculate TEMP_MIN_2_OUT - minimum of input4 and input5 *)
min_block(A := input4, B := input5);
TEMP_MIN_2_OUT := min_block.MIN_OUT;

(* Calculate TEMP_MIN_3_OUT - minimum of input2 and (input3 * TEMP_MIN_2_OUT + input2) *)
min_block(A := input2, B := (input3 * TEMP_MIN_2_OUT + input2));
TEMP_MIN_3_OUT := min_block.MIN_OUT;

(* Calculate N - minimum of input1 and (TEMP_MIN_3_OUT + input3) *)
min_block(A := input1, B := (TEMP_MIN_3_OUT + input3));
N := min_block.MIN_OUT;

(* Increment the CYCLE counter *)
UPDATED_CYCLE := CYCLE + 1;

END_FUNCTION_BLOCK
