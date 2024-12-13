
FUNCTION_BLOCK FB_Fibonacci_Calculator
VAR_INPUT
    N : INT;        (* Input: The term number for which Fibonacci is to be calculated *)
END_VAR

VAR_OUTPUT
    O : INT;        (* Output: The Fibonacci number at term N, with saturation *)
END_VAR

VAR
    F1 : INT := 1;  (* Variable to hold F(n-2) *)
    F2 : INT := 1;  (* Variable to hold F(n-1) *)
    F_next : INT;   (* Variable to hold the next Fibonacci number *)
    i : INT;        (* Loop index *)
END_VAR

O := 0;  (* Default the output to 0 *)

IF N <= 0 THEN
    O := 0;  (* Handle case for N less than or equal to 0 *)
ELSIF N = 1 THEN
    O := 1;  (* The first Fibonacci number *)
ELSE
    FOR i := 2 TO N DO
        F_next := F1 + F2;
        F1 := F2;
        F2 := F_next;
    END_FOR;
    O := F2;  (* The N-th Fibonacci number *)
END_IF;

END_FUNCTION_BLOCK
