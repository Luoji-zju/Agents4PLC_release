
FUNCTION_BLOCK TOGGLE_OUTPUT
VAR_INPUT
    Button : BOOL; // Input for the button state
END_VAR

VAR_OUTPUT
    ToggledOutput : BOOL; // Output that toggles based on button press
END_VAR

VAR
    PrevButtonState : BOOL; // Variable to track the previous state of the button
END_VAR

(* Check for rising edge of the button press *)
IF (Button = TRUE) AND (PrevButtonState = FALSE) THEN
    ToggledOutput := NOT ToggledOutput; // Toggle the output
END_IF

(* Update the previous button state for the next cycle *)
PrevButtonState := Button;

END_FUNCTION_BLOCK
