
FUNCTION_BLOCK FB_NestedLoops
VAR_INPUT
    flag : BOOL; (* Input flag to control loop execution *)
END_VAR

VAR_OUTPUT
    count : INT; (* Output variable to store the number of inner loop executions *)
END_VAR

VAR
    i : INT; (* Variable for outer loop iteration *)
    j : INT; (* Variable for inner loop iteration *)
    maxCount : INT := 45; (* Maximum expected iterations of the inner loop *)
END_VAR

(* Initialize count to 0 *)
count := 0;

(* Outer loop iterating from 0 to 10 *)
FOR i := 0 TO 10 DO
    (* Inner loop iterating from 10 to 100 with a step of 2 *)
    FOR j := 10 TO 100 BY 2 DO
        (* Check if the flag is TRUE *)
        IF flag THEN
            EXIT; (* Exit the inner loop if flag is TRUE *)
        END_IF;
        
        (* Increment the count for each inner loop execution *)
        count := count + 1;
        
        (* Ensure count does not exceed maxCount *)
        IF count >= maxCount THEN
            EXIT; (* Exit the inner loop if count exceeds maxCount *)
        END_IF;
    END_FOR;
    
    (* Check again if the flag is TRUE to exit the outer loop *)
    IF flag THEN
        EXIT; (* Exit the outer loop if flag is TRUE *)
    END_IF;
END_FOR;

END_FUNCTION_BLOCK
