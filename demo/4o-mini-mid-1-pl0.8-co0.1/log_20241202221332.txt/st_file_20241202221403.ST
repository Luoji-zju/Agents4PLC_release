
FUNCTION_BLOCK FB_Fibonacci_Calculator
VAR_INPUT
    N : INT; // Input value for Fibonacci calculation
END_VAR

VAR_OUTPUT
    O : INT; // Output value for the Fibonacci result
END_VAR

VAR
    F1 : INT := 1; // First Fibonacci number
    F2 : INT := 1; // Second Fibonacci number
    CNT : INT := 2; // Counter to track the position in the Fibonacci sequence
    NextFibonacci : INT; // Variable to hold the next Fibonacci number
END_VAR

(* Handle edge cases for N less than or equal to 2 *)
IF N <= 2 THEN
    O := 1;
    RETURN; // Exit the function if N is 2 or less
END_IF

(* Initialize the first two Fibonacci numbers *)
NextFibonacci := F1 + F2;

(* Calculate Fibonacci numbers iteratively *)
WHILE CNT < N DO
    IF NextFibonacci > 32767 THEN
        O := 32767; // Saturation condition
        RETURN; // Exit the function if saturation occurs
    END_IF

    F1 := F2; // Update F1 to the last F2
    F2 := NextFibonacci; // Update F2 to the next Fibonacci number
    NextFibonacci := F1 + F2; // Calculate the next Fibonacci number
    CNT := CNT + 1; // Increment the counter
END_WHILE

(* Assign the last calculated Fibonacci number to output O *)
O := F2; // Return the result
END_FUNCTION_BLOCK

(* Main PROGRAM to test the Fibonacci function block *)
PROGRAM prg
VAR_INPUT
    N : INT; // Input for Fibonacci calculation
END_VAR

VAR_OUTPUT
    Result : INT; // Output for the Fibonacci result
END_VAR

VAR
    fbFibonacci : FB_Fibonacci_Calculator; // Instance of the Fibonacci function block
END_VAR

(* Call the Fibonacci function block *)
fbFibonacci(N := N, O => Result);
END_PROGRAM
