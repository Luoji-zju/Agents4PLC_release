

FUNCTION_BLOCK FB_Fibonacci
VAR_INPUT
    N : INT; // The N-th Fibonacci number to calculate
END_VAR

VAR_OUTPUT
    O : INT; // Calculated Fibonacci number or 32767 if saturation occurs
END_VAR

VAR
    F1 : INT := 1; // First Fibonacci number
    F2 : INT := 1; // Second Fibonacci number
    CNT : INT; // Counter for iterations
    Temp : INT; // Temporary variable for calculations
END_VAR

// Main logic for calculating Fibonacci number
IF N <= 2 THEN
    O := 1; // Handle edge cases N <= 2
ELSE
    FOR CNT := 3 TO N DO
        Temp := F1 + F2; // Calculate the next Fibonacci number
        IF Temp > 32767 THEN
            O := 32767; // Saturation limit
            RETURN; // Exit the function block
        END_IF;
        F1 := F2; // Update F1
        F2 := Temp; // Update F2
        O := Temp; // Store the current Fibonacci number in O
    END_FOR;
END_IF;

END_FUNCTION_BLOCK

PROGRAM Main
VAR
    InputN : INT := 5; // Default input value for N
    Result : INT; // Variable to store the result
    fbFibonacci : FB_Fibonacci; // Instance of the Fibonacci function block
END_VAR

// Call the function block to compute the Fibonacci number
fbFibonacci(N := InputN, O => Result);

END_PROGRAM

