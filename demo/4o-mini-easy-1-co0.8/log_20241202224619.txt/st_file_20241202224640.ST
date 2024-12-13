
FUNCTION_BLOCK fb_dw
VAR_INPUT
    i : INT;  (* Input variable *)
END_VAR

VAR_OUTPUT
    o : INT;  (* Output variable *)
END_VAR

VAR
    ss : INT := 0;  (* Internal state variable initialized to 0 *)
END_VAR

(* Logic to determine output based on input and increment internal state *)
IF i = 1 THEN
    o := 1;  (* If input is 1, output is set to 1 *)
ELSE
    o := ss;  (* Otherwise, output is the current value of ss *)
END_IF;

ss := ss + 1;  (* Increment the internal state variable *)

END_FUNCTION_BLOCK

(* Test program to validate the functionality of the fb_dw function block *)
PROGRAM prg_test
VAR
    fb_instance : fb_dw;  (* Instance of the function block *)
    test_input : INT;  (* Variable to hold test input *)
    test_output : INT;  (* Variable to hold test output *)
END_VAR

(* Test execution with various input values *)
test_input := 1;
fb_instance(i := test_input, o => test_output);  (* Call the function block with input 1 *)
(* Expected output: 1 *)

test_input := 3;
fb_instance(i := test_input, o => test_output);  (* Call the function block with input 3 *)
(* Expected output: 0, as ss is initially 0 *)

fb_instance(i := test_input, o => test_output);  (* Call the function block again with the same input *)
(* Expected output: 1, as ss would have incremented to 1 after the first call *)

END_PROGRAM
