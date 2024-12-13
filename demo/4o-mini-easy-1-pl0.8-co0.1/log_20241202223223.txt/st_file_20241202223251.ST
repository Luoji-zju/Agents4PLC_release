
FUNCTION_BLOCK NOT_GATE
VAR_INPUT
    Input : BOOL; 
END_VAR_INPUT

VAR_OUTPUT
    NegatedOutput : BOOL;
END_VAR_OUTPUT

(* Implementing the negation logic *)
NegatedOutput := NOT Input;

END_FUNCTION_BLOCK
