
FUNCTION_BLOCK FB_NestedLoopControl
VAR_INPUT
    flag : BOOL;      (* Control flag to exit loops early *)
END_VAR_INPUT

VAR
    i : INT;          (* Outer loop index *)
    j : INT;          (* Inner loop index *)
    count : INT := 0; (* Count of inner loop iterations *)
    some_var : INT;   (* Additional variable if needed *)
END_VAR

(* Outer loop iterates from 0 to 10 *)
FOR i := 0 TO 10 DO
    (* Inner loop iterates from 10 to 100 with a step size of 2 *)
    FOR j := 10 TO 100 BY 2 DO
        
        (* Check if the exit flag is set *)
        IF flag THEN 
            EXIT;  (* Exit both loops if flag is TRUE *)
        END_IF
        
        (* Increment the count variable *)
        count := count + 1;
        
        (* Check if the count exceeds the defined maximum *)
        IF count > 100 THEN
            count := 100;  (* Cap the count at 100 *)
            EXIT;          (* Exit both loops if maximum is reached *)
        END_IF
        
    END_FOR;  (* End of inner loop *)
    
END_FOR;  (* End of outer loop *)

END_FUNCTION_BLOCK
