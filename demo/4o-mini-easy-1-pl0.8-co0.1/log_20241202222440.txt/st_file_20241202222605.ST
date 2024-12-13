
FUNCTION_BLOCK FB_LoopCounter
VAR_INPUT
    i : BOOL;  // Trigger input for the counter
END_VAR

VAR
    macro : INT := 0;  // Current count variable initialized to 0
    micro : INT := 0;  // Control variable for counting down initialized to 0
END_VAR

VAR_OUTPUT
    o : INT;  // Current value of the counter
END_VAR

// Check if the trigger input is true
IF i THEN
    // Decrement micro until it reaches zero
    IF micro > 0 THEN
        micro := micro - 1;
    ELSE
        // When micro reaches zero, increment macro and reset micro
        macro := macro + 1;
        micro := macro;  // Reset micro to the value of macro
    END_IF;
END_IF;

// Set the output variable to the current macro value
o := macro;

// Safeguard to ensure macro and micro do not become negative
IF macro < 0 THEN
    macro := 0;
END_IF;

IF micro < 0 THEN
    micro := 0;
END_IF;

END_FUNCTION_BLOCK
