
FUNCTION_BLOCK constantprogram
VAR_INPUT
    i : INT; (* Input integer variable *)
END_VAR

VAR_OUTPUT
    o : INT; (* Output integer variable, same as input *)
    c : INT; (* Constant output integer variable *)
END_VAR

(* Assign the input value to the output o *)
o := i;

(* Set the constant value to the output c *)
c := 43;

END_FUNCTION_BLOCK
