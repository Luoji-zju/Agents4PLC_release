
FUNCTION_BLOCK FIND_MAX_VALUE
VAR_INPUT
    Value1 : INT;  (* First integer input *)
    Value2 : INT;  (* Second integer input *)
END_VAR

VAR_OUTPUT
    MaxValue : INT;  (* Output for the maximum value *)
END_VAR

(* Compare the two input values and assign the larger one to MaxValue *)
IF Value1 > Value2 THEN
    MaxValue := Value1;  (* Value1 is greater *)
ELSE
    MaxValue := Value2;  (* Value2 is greater or they are equal *)
END_IF;

END_FUNCTION_BLOCK
