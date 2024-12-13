

FUNCTION_BLOCK AND_GATE
VAR_INPUT
    Input1 : BOOL;
    Input2 : BOOL;
END_VAR

VAR_OUTPUT
    AndResult : BOOL;
END_VAR

(* Implementing the AND logic operation *)
AndResult := Input1 AND Input2;

END_FUNCTION_BLOCK

