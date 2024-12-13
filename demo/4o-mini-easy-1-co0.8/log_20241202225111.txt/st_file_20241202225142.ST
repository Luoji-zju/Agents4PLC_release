
FUNCTION_BLOCK AND_GATE
VAR_INPUT
    Input1 : BOOL;  // First input for the AND gate
    Input2 : BOOL;  // Second input for the AND gate
END_VAR_INPUT

VAR_OUTPUT
    AndResult : BOOL;  // Result of the AND operation
END_VAR_OUTPUT

(* Implement the AND logic *)
AndResult := Input1 AND Input2;  // Perform the AND operation

END_FUNCTION_BLOCK

(* Test program for the AND_GATE function block *)
PROGRAM prg_AND_Test
VAR
    fb_AND : AND_GATE;  // Instance of the AND_GATE function block
    Test1 : BOOL;  // Test variable for Input1
    Test2 : BOOL;  // Test variable for Input2
    Result : BOOL;  // Variable to hold the result
END_VAR

(* Test all combinations of Input1 and Input2 *)
Test1 := TRUE; Test2 := TRUE; fb_AND(Input1 := Test1, Input2 := Test2); Result := fb_AND.AndResult;  // Expected: TRUE
Test1 := TRUE; Test2 := FALSE; fb_AND(Input1 := Test1, Input2 := Test2); Result := fb_AND.AndResult;  // Expected: FALSE
Test1 := FALSE; Test2 := TRUE; fb_AND(Input1 := Test1, Input2 := Test2); Result := fb_AND.AndResult;  // Expected: FALSE
Test1 := FALSE; Test2 := FALSE; fb_AND(Input1 := Test1, Input2 := Test2); Result := fb_AND.AndResult;  // Expected: FALSE

END_PROGRAM
