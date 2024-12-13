

FUNCTION_BLOCK TOGGLE_OUTPUT
VAR_INPUT
    Button : BOOL; // Input indicating the button state (pressed or not pressed)
END_VAR

VAR_OUTPUT
    ToggledOutput : BOOL; // Output indicating the toggled state
END_VAR

VAR
    PrevButtonState : BOOL := FALSE; // Local variable to track the previous button state
END_VAR

// Check for transition from not pressed (FALSE) to pressed (TRUE)
IF (Button = TRUE) AND (PrevButtonState = FALSE) THEN
    // Toggle the output
    ToggledOutput := NOT ToggledOutput;
END_IF;

// Update the previous button state
PrevButtonState := Button;

END_FUNCTION_BLOCK

