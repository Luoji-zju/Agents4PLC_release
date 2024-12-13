
FUNCTION_BLOCK dw
VAR_INPUT
    i : INT;  (* Input variable *)
END_VAR

VAR_OUTPUT
    o : INT;  (* Output variable *)
END_VAR

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
