
FUNCTION_BLOCK constantprogram
VAR_INPUT
    i : INT; (* Input integer *)
END_VAR

VAR_OUTPUT
    o : INT; (* Output integer equal to input *)
    c : INT; (* Output constant integer *)
END_VAR

(* Assign input to output *)
o := i;

(* Assign constant value to output *)
c := 43;

END_FUNCTION_BLOCK
