
FUNCTION_BLOCK FB_Fibonacci_Calculator
VAR_INPUT
    N : INT := 5; (* Default value for N is 5 *)
END_VAR

VAR_OUTPUT
    O : INT; (* Output variable for the Fibonacci number *)
END_VAR

VAR
    F1 : INT := 1; (* First Fibonacci number *)
    F2 : INT := 1; (* Second Fibonacci number *)
    CNT : INT := 2; (* Counter initialized to 2 since F1 and F2 are the first two terms *)
    Temp : INT; (* Temporary variable for calculation *)
END_VAR

(* Handle edge cases where N <= 2 *)
IF N <= 2 THEN
    O := 1;
ELSE
    (* Calculate Fibonacci numbers up to the N-th term *)
    WHILE CNT < N DO
        Temp := F1 + F2;
        
        (* Implement saturation arithmetic *)
        IF Temp > 32767 THEN
            O := 32767;
            EXIT; (* Exit the loop if saturation occurs *)
        END_IF;
        
        F1 := F2;
        F2 := Temp;
        CNT := CNT + 1;
    END_WHILE;
    
    O := F2; (* Set the output to the N-th Fibonacci number *)
END_IF;
END_FUNCTION_BLOCK
