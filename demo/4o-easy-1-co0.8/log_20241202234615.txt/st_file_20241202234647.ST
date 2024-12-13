
FUNCTION_BLOCK FIND_MAX_VALUE
VAR_INPUT
    Value1 : INT;   (* First integer input *)
    Value2 : INT;   (* Second integer input *)
END_VAR

VAR_OUTPUT
    MaxValue : INT; (* Output to hold the maximum value *)
END_VAR

(* Use IF-THEN-ELSE statement to determine the maximum value *)
IF Value1 > Value2 THEN
    MaxValue := Value1;
ELSE
    MaxValue := Value2;
END_IF;

END_FUNCTION_BLOCK
