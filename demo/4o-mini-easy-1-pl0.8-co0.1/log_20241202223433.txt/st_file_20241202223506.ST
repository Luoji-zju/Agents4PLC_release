
FUNCTION_BLOCK OR_GATE
VAR_INPUT
    Input1 : BOOL; 
    Input2 : BOOL; 
END_VAR

VAR_OUTPUT
    OrResult : BOOL; 
END_VAR

(* Implementing the OR logic *)
OrResult := Input1 OR Input2;

END_FUNCTION_BLOCK

FUNCTION_BLOCK NOT_GATE
VAR_INPUT
    Input1 : BOOL; 
END_VAR

VAR_OUTPUT
    NotResult : BOOL; 
END_VAR

(* Implementing the NOT logic *)
NotResult := NOT Input1;

END_FUNCTION_BLOCK

FUNCTION_BLOCK XOR_GATE
VAR_INPUT
    Input1 : BOOL; 
    Input2 : BOOL; 
END_VAR

VAR_OUTPUT
    XorResult : BOOL; 
END_VAR

(* Implementing the XOR logic using AND and NOT operators *)
XorResult := (Input1 AND NOT Input2) OR (NOT Input1 AND Input2);

END_FUNCTION_BLOCK

