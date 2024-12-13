
FUNCTION USER_MAX : INT
VAR_INPUT
    A : INT;
    B : INT;
END_VAR
BEGIN
    IF A > B THEN
        USER_MAX := A;
    ELSE
        USER_MAX := B;
    END_IF;
END_FUNCTION

FUNCTION USER_MIN : INT
VAR_INPUT
    A : INT;
    B : INT;
END_VAR
BEGIN
    IF A < B THEN
        USER_MIN := A;
    ELSE
        USER_MIN := B;
    END_IF;
END_FUNCTION

FUNCTION_BLOCK FB_ValueComparison
VAR_INPUT
    input1 : INT;
    input2 : INT;
    input3 : INT;
    input4 : INT;
    input5 : INT;
END_VAR_INPUT

VAR_OUTPUT
    M : INT;  (* Maximum value *)
    N : INT;  (* Minimum value *)
    UPDATED_CYCLE : INT;  (* Cycle counter *)
END_VAR_OUTPUT

VAR
    TEMP_MAX_OUT : INT;
    TEMP_MIN_2_OUT : INT;
    TEMP_MIN_3_OUT : INT;
END_VAR

(* Initialize cycle counter *)
IF UPDATED_CYCLE = 0 THEN
    UPDATED_CYCLE := 1;  (* Start counting from 1 *)
ELSE
    UPDATED_CYCLE := UPDATED_CYCLE + 1;  (* Increment cycle counter *)
END_IF;

(* Calculate maximum value *)
TEMP_MAX_OUT := USER_MAX(input2, input3);
M := USER_MAX(input1, TEMP_MAX_OUT);

(* Calculate minimum value *)
TEMP_MIN_2_OUT := USER_MIN(input4, input5);
TEMP_MIN_3_OUT := USER_MIN(input2, (input3 * TEMP_MIN_2_OUT + input2));
N := USER_MIN(input1, TEMP_MIN_3_OUT + input3);

END_FUNCTION_BLOCK
