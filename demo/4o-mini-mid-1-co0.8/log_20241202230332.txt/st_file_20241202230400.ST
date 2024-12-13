
FUNCTION_BLOCK FB_Fibonacci_Calculator
VAR_INPUT
    N : INT;        (* Input: The term number for which Fibonacci is to be calculated *)
END_VAR_INPUT

VAR_OUTPUT
    O : INT;        (* Output: The Fibonacci number at term N, with saturation *)
END_VAR_OUTPUT

VAR
    F1 : INT := 1;  (* Variable to hold F(n-2) *)
    F2 : INT := 1;  (* Variable to hold F(n-1) *)
    F_next : INT;   (* Variable to hold the next Fibonacci number *)
    i : INT;        (* Loop index *)
END_VAR

(* Handle edge cases where N is less than or equal to 2 *)
IF N <= 2 THEN
    O := 1;  (* For N = 1 or N = 2, output is 1 *)
ELSE
    O := 0;  (* Initialize output *)
    FOR i := 3 TO N DO
        F_next := F1 + F2;  (* Calculate next Fibonacci number *)
        
        (* Implement saturation arithmetic *)
        IF F_next > 32767 THEN
            O := 32767;  (* Cap the output at 32767 *)
            RETURN;      (* Exit the function block *)
        ELSE
            O := F_next;  (* Update output with calculated Fibonacci number *)
        END_IF
        
        (* Update F1 and F2 for next iteration *)
        F1 := F2;  (* Move F(n-1) to F(n-2) *)
        F2 := F_next;  (* Move F(n) to F(n-1) *)
    END_FOR
END_IF

END_FUNCTION_BLOCK

