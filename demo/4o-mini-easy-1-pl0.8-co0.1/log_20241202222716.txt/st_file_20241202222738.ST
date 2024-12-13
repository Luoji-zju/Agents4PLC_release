
FUNCTION_BLOCK FB_ValueTracker
VAR_INPUT
    aaa : INT := 1;          // Initialize aaa to 1
    bbb : INT := 0;          // Initialize bbb to 0
END_VAR

VAR_OUTPUT
    OUT : INT;               // Output variable for the difference
    UPDATED_CYCLE : INT;     // Output variable for the updated cycle count
END_VAR

VAR
    CYCLE : INT := 0;        // Cycle counter initialized to 0
END_VAR

(* Main logic to compare and increment values *)
IF aaa > bbb THEN
    bbb := bbb + 1;         // Increment bbb if aaa is greater
ELSIF aaa < bbb THEN
    aaa := aaa + 1;         // Increment aaa if bbb is greater
END_IF

OUT := aaa - bbb;           // Calculate the difference between aaa and bbb
CYCLE := CYCLE + 1;        // Increment the cycle counter
UPDATED_CYCLE := CYCLE;    // Update the output cycle count

END_FUNCTION_BLOCK
