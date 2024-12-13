
FUNCTION_BLOCK FB_LoopCounter
VAR_INPUT
    i : BOOL;  // Trigger input for the counter
END_VAR

VAR
    macro : INT := 1;  // Current count
    micro : INT := 1;  // Control variable for counting down
END_VAR

VAR_OUTPUT
    o : INT;  // Current value of the counter
END_VAR

// Logic to manage loop counter
IF i THEN
    // Decrement the micro variable if it is greater than 0
    IF micro > 0 THEN
        micro := micro - 1;
    END_IF;

    // Check if micro has reached zero
    IF micro = 0 THEN
        macro := macro + 1; // Increment macro variable
        micro := macro;     // Reset micro to the value of macro
    END_IF;
END_IF;

// Assign the current count to output variable
o := macro;

END_FUNCTION_BLOCK

PROGRAM prg
VAR_INPUT
    trigger : BOOL;  // Input trigger for the loop counter
END_VAR

VAR
    loopCounter : FB_LoopCounter; // Instance of the loop counter function block
END_VAR

// Call the loop counter function block with the trigger input
loopCounter(i := trigger);

END_PROGRAM
