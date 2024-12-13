
FUNCTION_BLOCK NOT_GATE
VAR_INPUT
    Input : BOOL;
END_VAR

VAR_OUTPUT
    NegatedOutput : BOOL;
END_VAR

(* Logic to simulate a NOT gate *)
NegatedOutput := NOT Input;

END_FUNCTION_BLOCK
