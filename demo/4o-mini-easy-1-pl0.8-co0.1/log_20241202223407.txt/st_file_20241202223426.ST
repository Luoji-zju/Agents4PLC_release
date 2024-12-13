
FUNCTION_BLOCK NOT_GATE
VAR_INPUT
    Input : BOOL; 
END_VAR

VAR_OUTPUT
    NegatedOutput : BOOL;
END_VAR

(* Implementing the logical negation of the input *)
NegatedOutput := NOT Input;

END_FUNCTION_BLOCK
