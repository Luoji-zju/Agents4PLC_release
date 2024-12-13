
FUNCTION_BLOCK CALCULATE_OUTPUT
VAR_INPUT
    i : INT; (* Input integer *)
END_VAR

VAR_OUTPUT
    o : INT; (* Output integer *)
END_VAR

VAR
    result : INT; (* Local variable for intermediate calculations *)
END_VAR

(* Implementing conditional logic to determine the output based on input 'i' *)
IF i = 0 THEN
    result := 0;
ELSIF i >= 1 AND i <= 5 THEN
    result := i * i; (* Square of 'i' *)
ELSIF i >= 6 AND i <= 10 THEN
    result := i + (2 * i); (* 'i' plus two times 'i' *)
ELSE
    result := -1; (* Default case for inputs outside the specified ranges *)
END_IF;

(* Assign the calculated result to the output variable 'o' *)
o := result;

END_FUNCTION_BLOCK
