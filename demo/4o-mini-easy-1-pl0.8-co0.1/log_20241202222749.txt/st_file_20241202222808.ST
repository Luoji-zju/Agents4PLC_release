
FUNCTION_BLOCK constantprogram
VAR_INPUT
    i : INT;  (* Input variable to receive the integer value *)
END_VAR

VAR_OUTPUT
    o : INT;  (* Output variable to store the input value *)
    c : INT;  (* Output variable to store the constant value *)
END_VAR

(* Main logic section of the function block *)
o := i;  (* Assign the input value to output o *)
c := 43; (* Assign the constant value 43 to output c *)

END_FUNCTION_BLOCK
