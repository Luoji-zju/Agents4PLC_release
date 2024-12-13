
FUNCTION_BLOCK AND_GATE
VAR_INPUT
    Input1 : BOOL; 
    Input2 : BOOL; 
END_VAR

VAR_OUTPUT
    AndResult : BOOL;
END_VAR

(* Implement the AND logic *)
AndResult := Input1 AND Input2;

END_FUNCTION_BLOCK

PROGRAM prg
VAR_INPUT
    input1_test : BOOL;
    input2_test : BOOL;
END_VAR

VAR
    and_gate: AND_GATE;
    result: BOOL;
END_VAR

(* Test the AND_GATE function block with various combinations of boolean inputs *)
and_gate(Input1 := input1_test, Input2 := input2_test, AndResult => result);

END_PROGRAM
