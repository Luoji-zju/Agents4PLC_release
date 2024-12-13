
FUNCTION_BLOCK constantprogram
VAR_INPUT
    i : INT; 
END_VAR

VAR_OUTPUT
    o : INT;
    c : INT;
END_VAR

(* Assign the input value to output variable 'o' *)
o := i;

(* Assign constant value to output variable 'c' *)
c := 43;

END_FUNCTION_BLOCK
