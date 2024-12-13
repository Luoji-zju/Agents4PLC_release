
FUNCTION_BLOCK AND_GATE
VAR_INPUT
    Input1 : BOOL;  (* First boolean input *)
    Input2 : BOOL;  (* Second boolean input *)
END_VAR

VAR_OUTPUT
    AndResult : BOOL;  (* Output of the AND gate *)
END_VAR

(* Implementing the logic for the AND gate *)
AndResult := Input1 AND Input2;

END_FUNCTION_BLOCK

(* Main PROGRAM to test the AND_GATE function block *)
PROGRAM prg
VAR
    fb_AND : AND_GATE;  (* Instance of the AND_GATE function block *)
    result : BOOL;      (* Variable to hold the result *)
END_VAR

(* Test cases *)
(* Test Case 1: Input1 = TRUE, Input2 = TRUE *)
fb_AND(Input1 := TRUE, Input2 := TRUE);
result := fb_AND.AndResult;  (* Expected: TRUE *)

(* Test Case 2: Input1 = TRUE, Input2 = FALSE *)
fb_AND(Input1 := TRUE, Input2 := FALSE);
result := fb_AND.AndResult;  (* Expected: FALSE *)

(* Test Case 3: Input1 = FALSE, Input2 = TRUE *)
fb_AND(Input1 := FALSE, Input2 := TRUE);
result := fb_AND.AndResult;  (* Expected: FALSE *)

(* Test Case 4: Input1 = FALSE, Input2 = FALSE *)
fb_AND(Input1 := FALSE, Input2 := FALSE);
result := fb_AND.AndResult;  (* Expected: FALSE *)

END_PROGRAM
