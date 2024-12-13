
FUNCTION_BLOCK dw
VAR_INPUT
    i : INT;  (* Input variable *)
END_VAR_INPUT

VAR_OUTPUT
    o : INT;  (* Output variable *)
END_VAR_OUTPUT

VAR
    ss : INT := 0;  (* Internal state variable initialized to 0 *)
END_VAR

(* Increment the internal state variable on each execution *)
ss := ss + 1;

(* Conditional logic to determine output based on input *)
IF i = 1 THEN
    o := 1;  (* If input is 1, output is set to 1 *)
ELSE
    o := ss;  (* Otherwise, output is the current value of ss *)
END_IF;

END_FUNCTION_BLOCK

(* Main PROGRAM to test the Function Block *)
PROGRAM prg
VAR
    fb_dw : dw;  (* Instance of the Function Block *)
    input_value : INT;  (* Variable to hold input value *)
    output_value : INT;  (* Variable to hold output value *)
END_VAR

(* Example of calling the Function Block with different inputs *)
input_value := 1;  (* Test input *)
fb_dw(i := input_value, o => output_value);  (* Call the Function Block *)
(* output_value should now be 1 *)

input_value := 2;  (* Next test input *)
fb_dw(i := input_value, o => output_value);  (* Call the Function Block *)
(* output_value should now be 2, as ss was incremented *)

input_value := 2;  (* Another test input *)
fb_dw(i := input_value, o => output_value);  (* Call the Function Block *)
(* output_value should now be 3, as ss was incremented again *)

END_PROGRAM
