
FUNCTION_BLOCK AND_GATE
VAR_INPUT
    Input1 : BOOL;  // First input for the AND gate
    Input2 : BOOL;  // Second input for the AND gate
END_VAR

VAR_OUTPUT
    AndResult : BOOL;  // Result of the AND operation
END_VAR

(* Implement the AND logic *)
AndResult := Input1 AND Input2;  // Perform the AND operation

END_FUNCTION_BLOCK
