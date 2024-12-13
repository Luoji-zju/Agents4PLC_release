

(* Function block for a NOT gate *)
FUNCTION_BLOCK NOT_GATE
VAR_INPUT
    Input : BOOL; (* Input variable for the NOT gate *)
END_VAR

VAR_OUTPUT
    NegatedOutput : BOOL; (* Output variable for the NOT gate *)
END_VAR

(* Logic to negate the input *)
NegatedOutput := NOT Input;

END_FUNCTION_BLOCK

(* Function block for an AND gate *)
FUNCTION_BLOCK AND_GATE
VAR_INPUT
    Input1 : BOOL; (* First input variable for the AND gate *)
    Input2 : BOOL; (* Second input variable for the AND gate *)
END_VAR

VAR_OUTPUT
    AndOutput : BOOL; (* Output variable for the AND gate *)
END_VAR

(* Logic to perform AND operation on the inputs *)
AndOutput := Input1 AND Input2;

END_FUNCTION_BLOCK

(* Function block for an OR gate *)
FUNCTION_BLOCK OR_GATE
VAR_INPUT
    Input1 : BOOL; (* First input variable for the OR gate *)
    Input2 : BOOL; (* Second input variable for the OR gate *)
END_VAR

VAR_OUTPUT
    OrOutput : BOOL; (* Output variable for the OR gate *)
END_VAR

(* Logic to perform OR operation on the inputs *)
OrOutput := Input1 OR Input2;

END_FUNCTION_BLOCK

