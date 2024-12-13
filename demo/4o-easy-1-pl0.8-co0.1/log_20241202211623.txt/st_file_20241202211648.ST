

FUNCTION_BLOCK FIND_MAX_VALUE
VAR_INPUT
    Value1 : INT;
    Value2 : INT;
END_VAR

VAR_OUTPUT
    MaxValue : INT;
END_VAR

(* Compare the two input values and assign the larger one to MaxValue *)
IF Value1 > Value2 THEN
    MaxValue := Value1;
ELSE
    MaxValue := Value2;
END_IF;

END_FUNCTION_BLOCK

