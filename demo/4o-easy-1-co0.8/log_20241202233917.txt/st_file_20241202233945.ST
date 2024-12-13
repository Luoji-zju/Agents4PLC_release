
FUNCTION_BLOCK FB_LoopCounter
VAR_INPUT
    flag : BOOL;
END_VAR

VAR_OUTPUT
    count : INT;
END_VAR

VAR
    i : INT;
    j : INT;
    maxIterations : INT := 45; (* Maximum expected iterations for the inner loop *)
END_VAR

(* Initialize count to zero *)
count := 0;

(* Outer loop iterating from 0 to 10 *)
FOR i := 0 TO 10 DO
    (* Inner loop iterating from 10 to 100 with a step size of 2 *)
    FOR j := 10 TO 100 BY 2 DO
        (* Check the flag, if TRUE, exit the inner loop *)
        IF flag THEN
            EXIT;
        END_IF;
        
        (* Increment the count for each execution of the inner loop *)
        count := count + 1;
        
        (* Ensure count does not exceed the maximum expected iterations *)
        IF count >= maxIterations THEN
            EXIT;
        END_IF;
    END_FOR;
END_FOR;

END_FUNCTION_BLOCK
