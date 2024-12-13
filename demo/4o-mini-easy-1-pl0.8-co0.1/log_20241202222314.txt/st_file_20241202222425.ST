
FUNCTION_BLOCK FB_NestedLoopControl
VAR
    flag : BOOL;  (* Control flag to exit loops *)
    i : INT;      (* Outer loop index *)
    j : INT;      (* Inner loop index *)
    count : INT := 0;  (* Count of inner loop executions *)
    max_count : INT := 46;  (* Maximum allowed count *)
END_VAR

(* Outer loop iterating from 0 to 10 *)
FOR i := 0 TO 10 DO
    (* Inner loop iterating from 10 to 100 with a step size of 2 *)
    FOR j := 10 TO 100 BY 2 DO
        (* Check if the exit flag is set to TRUE *)
        IF flag THEN
            EXIT;  (* Exit the inner loop if flag is TRUE *)
        END_IF
        
        (* Increment the count for each iteration of the inner loop *)
        count := count + 1;

        (* Ensure count does not exceed the defined maximum *)
        IF count > max_count THEN
            count := max_count;  (* Cap the count at maximum *)
            EXIT;  (* Exit the inner loop if maximum is reached *)
        END_IF
    END_FOR;  (* End of inner loop *)
END_FOR;  (* End of outer loop *)

END_FUNCTION_BLOCK
