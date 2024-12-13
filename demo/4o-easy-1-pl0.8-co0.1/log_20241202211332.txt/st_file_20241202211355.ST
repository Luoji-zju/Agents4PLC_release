

FUNCTION_BLOCK dw
VAR_INPUT
    i : INT; (* Input variable *)
END_VAR

VAR_OUTPUT
    o : INT; (* Output variable *)
END_VAR

VAR
    ss : INT := 0; (* Internal variable to keep track of state *)
END_VAR

(* Increment the internal state variable ss each time the block is executed *)
ss := ss + 1;

(* Conditional logic to determine the output based on the input *)
IF i = 1 THEN
    o := 1;
ELSE
    o := ss;
END_IF;

END_FUNCTION_BLOCK

